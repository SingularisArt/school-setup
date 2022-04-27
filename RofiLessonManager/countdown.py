#!/usr/bin/python3

"""
This class is used to create a calendar.
- If we are not in a class:
    - Check if we have any classes left for the day:
        - If we do:
            (CLASS NAME) in (TIME REMAINING) at (CLASS LOCATION)
        - If we don't:
            No classes left for today
- If we are in a class:
    (CLASS NAME) ends in (TIME REMAINING)
    - It also changes the current course automatically
"""

import pickle

import sys
import os
import os.path

import yaml

import re
import math

import sched
import datetime
import time
import pytz
from dateutil.parser import parse

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import http.client as httplib

from RofiLessonManager import Basis as Basis
from RofiLessonManager.change_course import ChangeCourse
from RofiLessonManager.view_lessons import ViewLectures


class Calendar(Basis):
    """
    This class is used to manage my calendar.
    It creates, removes, and updates my school events.
    It also notifies me about my upcoming classes and changes my current course
    accordingly.
    """

    def __init__(self):
        """
        Initializes the calendar.
        """

        super().__init__()

        self.TZ = ''
        if 'TZ' in os.environ:
            self.TZ = pytz.timezone(os.environ['TZ'])
        else:
            print("Warning: TZ environ variable not set")

        self.calendar_id = 'primary'
        self.now = datetime.datetime.now(tz=self.TZ)

        self.morning = self.now.replace(hour=6, minute=0, microsecond=0)
        self.evening = self.now.replace(hour=23, minute=59, microsecond=0)

        self.courses = ChangeCourse()
        self.lectures = ViewLectures()
        self.service = self.authenticate()
        self.events = self.get_events('primary')

    def truncate(self, string, length=35):
        ellipsis = ' ...'
        if len(string) < length:
            return string
        return string[:length - len(ellipsis)] + ellipsis

    def summary(self, text):
        return self.truncate(re.sub(r'X[0-9A-Za-z]+', '', text).strip(), 50)

    def gray(self, text):
        return '%{F#999999}' + text + '%{F-}'

    def formatdd(self, begin, end):
        minutes = math.ceil((end - begin).seconds / 60)

        if minutes == 1:
            return '1 minute'

        if minutes < 60:
            return '{} min'.format(minutes)

        hours = math.floor(minutes/60)
        rest_minutes = minutes % 60

        if hours == 1:
            return '1 hour'
        if hours > 5 or rest_minutes == 0:
            return '{} hours'.format(hours)

        return '{}:{:02d} hours'.format(hours, rest_minutes)

    def location(self, text):
        if not text:
            return ''
        match = re.search(r'\((.*)\)', text)

        if not match:
            return ''

        return f'{self.gray("in")} {match.group(1)}'

    def join(self, *args):
        return ' '.join(str(e) for e in args if e)

    def text(self, events, now):
        current = next((e for e in events
                        if e['start'] < now and now < e['end']), None)

        if not current:
            nxt = next((e for e in events if now <= e['start']), None)
            if nxt:
                return self.join(
                    self.summary(nxt['summary']),
                    self.gray('ends in'),
                    self.formatdd(now, nxt['start']),
                    self.location(nxt['location'])
                )
            return ''

        nxt = next((e for e in events if e['start'] >= current['end']), None)
        if not nxt:
            return self.join(self.gray('{} ends in'.format(
                current['summary'])),
                   self.formatdd(now, current['end']) + '!')

        if current['end'] == nxt['start']:
            return self.join(
                self.gray('{} ends in'.format(current['summary'])),
                self.formatdd(now, current['end']) + self.gray('.'),
                self.gray('After this'),
                self.summary(nxt['summary']),
                self.location(nxt['location'])
            )

        return self.join(
            self.gray('{} ends in'.format(current['summary'])),
            self.formatdd(now, current['end']) + self.gray('.'),
            self.gray('After this'),
            self.summary(nxt['summary']),
            self.location(nxt['location']),
            self.gray('After a break of'),
            self.formatdd(current['end'], nxt['start'])
        )

    def authenticate(self):
        print('Authenticating ...')
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        creds = None
        # The file token.pickle stores the user's access and refresh tokens,
        # and is created automatically when the authorization flow completes
        # for the first time.
        if os.path.exists('token.pickle'):
            with open('{}/token.pickle'.format(self.code_dir), 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print('Refreshing credentials')
                creds.refresh(Request())
            else:
                print('Need to allow access')
                flow = InstalledAppFlow.from_client_secrets_file(
                        '{}/credentials.json'.format(self.code_dir), SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('{}/token.pickle'.format(self.code_dir), 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
        return service

    def get_events(self, calendar):
        events_result = self.service.events().list(
            calendarId=calendar,
            timeMin=self.morning.isoformat(),
            timeMax=self.evening.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        return [
            {
                'summary': event['summary'],
                'location': event.get('location', None),
                'start': parse(event['start']['dateTime']),
                'end': parse(event['end']['dateTime'])
            }
            for event in events
            if 'dateTime' in event['start']
        ]

    def activate_course(self, event):
        for i, course in enumerate(self.courses.classes):
            info = open('{}/info.yaml'.format(course))
            file_info = yaml.load(info, Loader=yaml.FullLoader)

            if file_info['calendar_name'] == event['summary']:
                self.courses.activate(i)
                return 'Activated {}'.format(event['summary'])
            elif file_info['title'] == event['summary']:
                self.courses.activate(i)
                return 'Activated {}'.format(event['summary'])


def main():
    scheduler = sched.scheduler(time.time, time.sleep)
    cal = Calendar()

    print('Initializing')
    TZ = pytz.timezone(os.environ['TZ'])
    if 'TZ' in os.environ:
        TZ = pytz.timezone(os.environ['TZ'])
    else:
        print("Warning: TZ environ variable not set")

    service = cal.authenticate()

    print('Authenticated')
    print('Searching for events')

    # Call the Calendar API
    def get_events(calendar):
        events_result = service.events().list(
            calendarId=calendar,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        return [
            {
                'summary': event['summary'],
                'location': event.get('location', None),
                'start': parse(event['start']['dateTime']),
                'end': parse(event['end']['dateTime'])
            }
            for event in events
            if 'dateTime' in event['start']
        ]

    events = get_events('primary')
    print('Done')

    DELAY = 60

    def print_message():
        now = datetime.datetime.now(tz=TZ)
        print(cal.text(events, now))
        if now < cal.evening:
            scheduler.enter(DELAY, 1, print_message)

    for event in events:
        # absolute entry, priority 1
        scheduler.enterabs(event['start'].timestamp(), 1, cal.activate_course,
                           argument=(event, ))

    # Immediate, priority 1
    scheduler.enter(0, 1, print_message)
    scheduler.run()


def wait_for_internet_connection(url, timeout=1):
    while True:
        conn = httplib.HTTPConnection(url, timeout=5)
        try:
            conn.request("HEAD", "/")
            conn.close()
            return True
        except httplib.HTTPException:
            conn.close()


if __name__ == '__main__':
    os.chdir(sys.path[0])
    print('Waiting for connection')
    wait_for_internet_connection('www.google.com')
    main()
