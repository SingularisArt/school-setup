#!/usr/bin/python3
import pickle

import os
import os.path
import sys

import math
import re

import sched
import datetime
import time
import pytz
from dateutil.parser import parse

import urllib.request

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

from RofiLessonManager.courses import Courses as Courses
import RofiLessonManager.utils as utils

courses = Courses()


def authenticate():
    print('Authenticating')
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                return
        else:
            print('3')
            print('Need to allow access')
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            print('4')
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def formatdd(begin, end):
    minutes = math.ceil((end - begin).seconds / 60)

    if minutes == 1:
        return '1 minute'

    if minutes < 60:
        return '{} minutes'.format(minutes)

    hours = math.floor(minutes/60)
    rest_minutes = minutes % 60

    if hours == 1 and rest_minutes == 0:
        return '1 hour'
    elif hours > 5 or rest_minutes == 0:
        return '{} hours'.format(hours)

    return '{}:{:02d} hours'.format(hours, rest_minutes)


def text(events, now, end):
    current = next(
        (e for e in events if e['start'] < now and now < e['end']), None)

    # Check if we have an event right now
    if not current:
        nxt = next((e for e in events if now <= e['start']), None)
        if nxt:
            return utils.join(
                utils.summary(nxt['summary']),
                utils.colored_text('starts in'),
                formatdd(now, nxt['start']),
                utils.location(nxt['location']),
                '   ',
                utils.format_time(nxt['start'])
            )
        return ''
    nxt = next((e for e in events if e['start'] >= current['end']), None)
    if not nxt:
        return utils.join(utils.colored_text('Ends in'),
                          formatdd(now, current['end']) + '!',
                          '   ',
                          utils.format_time(current['end'])
                          )

    if current['end'] == nxt['start']:
        return utils.join(
            utils.colored_text('Ends in'),
            formatdd(now, current['end']) + utils.colored_text('.'),
            utils.colored_text('Next:'),
            utils.summary(nxt['summary']),
            utils.location(nxt['location']),
            '   ',
            utils.format_time(nxt['start'])
        )

    return utils.join(
        utils.colored_text('Ends in'),
        formatdd(now, current['end']) + utils.colored_text('.'),
        utils.colored_text('Next:'),
        utils.summary(nxt['summary']),
        utils.location(nxt['location']),
        utils.colored_text('after a'),
        formatdd(current['end'], nxt['start']),
        utils.colored_text('break.'),
        '   ',
        utils.format_time(current['end'])
    )


def activate_course(event):
    course = next(
        (course for course in courses
         if course.info['title'].lower() in event['summary'].lower()),
        None
    )

    if not course:
        return

    if course.info['title'] == event['summary']:
        courses.current = course


def main(end=False):
    scheduler = sched.scheduler(time.time, time.sleep)

    print('Initializing')
    if 'TZ' in os.environ:
        TZ = pytz.timezone(os.environ['TZ'])
    else:
        print("Warning: TZ environ variable not set")

    service = authenticate()

    print('Authenticated')
    # Call the Calendar API
    now = datetime.datetime.now(tz=TZ)

    morning = now.replace(hour=6, minute=0, microsecond=0)
    evening = now.replace(hour=23, minute=59, microsecond=0)

    print('Searching for events')

    def get_events(calendar):
        events_result = service.events().list(
            calendarId=calendar,
            timeMin=morning.isoformat(),
            timeMax=evening.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        new_events = []
        for event in events:
            try:
                summary = re.search('(.+) \(CLASS\)', event['summary']).group(1)
                event_dict = {
                    'summary': summary,
                    'location': event.get('location', None),
                    'start': parse(event['start']['dateTime']),
                    'end': parse(event['end']['dateTime'])
                }
                new_events.append(event_dict)
            except Exception:
                pass

        # return [
        #     {
        #         'summary': event['summary'],
        #         'location': event.get('location', None),
        #         'start': parse(event['start']['dateTime']),
        #         'end': parse(event['end']['dateTime'])
        #     }
        #     for event in events
        #     if 'dateTime' in event['start']
        # ]
        return new_events

    events = get_events(courses.calendar_id)
    print('Done')

    DELAY = 60

    def print_message():
        now = datetime.datetime.now(tz=TZ)
        print(text(events, now, end))
        if now < evening:
            scheduler.enter(DELAY, 1, print_message)

    for event in events:
        # absolute entry, priority 1
        scheduler.enterabs(event['start'].timestamp(),
                           1, activate_course, argument=(event, ))

    # Immediate, priority 1
    scheduler.enter(0, 1, print_message)
    scheduler.run()


def check_internet(host='http://google.com'):
    while True:
        try:
            urllib.request.urlopen(host)
            break
        except:
            pass


if __name__ == '__main__':
    os.chdir(sys.path[0])
    print('Waiting for connection')
    check_internet()
    main()
