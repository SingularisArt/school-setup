#!/usr/bin/python3

import pickle

import os
import os.path
import sys

import re
import math

import sched
import datetime
import time
import pytz
from dateutil.parser import parse

import http.client as httplib

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from RofiLessonManager.courses import Courses as Courses

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
            print('Refreshing credentials')
            creds.refresh(Request())
        else:
            print('Need to allow access')
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def join(*args):
    return ' '.join(str(e) for e in args if e)


def truncate(string, length):
    ellipsis = ' ...'
    if len(string) < length:
        return string
    return string[:length - len(ellipsis)] + ellipsis


def summary(text):
    return truncate(re.sub(r'X[0-9A-Za-z]+', '', text).strip(), 50)


def colored_text(text, color='#999999'):
    return '%{F' + color + '}' + text + '%{F-}'


def formatdd(begin, end):
    minutes = math.ceil((end - begin).seconds / 60)

    if minutes == 1:
        return '1 minute'

    if minutes < 60:
        return '{} minutes'.format(minutes)

    hours = math.floor(minutes/60)
    rest_minutes = minutes % 60

    if hours > 5 or rest_minutes == 0:
        return '{} hours'.format(hours)
    if hours == 1:
        return '1 hour and {} minutes'.format(rest_minutes)

    return '{} hours {:02d} minutes'.format(hours, rest_minutes)


def location(text):
    if not text:
        return ''

    return '{} {}'.format(colored_text("in"), text)


def text(events, now):
    current = next(
        (e for e in events if e['start'] < now and now < e['end']), None)

    if not current:
        nxt = next((e for e in events if now <= e['start']), None)
        if nxt:
            color_id = ''
            try:
                color_id = nxt['colorId']
            except Exception:
                color_id = 'None'

            return join(
                get_color_from_id(color_id, summary(nxt['summary'])),
                colored_text('starts'),
                formatdd(now, nxt['start']),
                location(nxt['location'])
            )
        return ''

    nxt = next((e for e in events if e['start'] >= current['end']), None)
    if not nxt:
        return join(colored_text('Ends in'),
                    formatdd(now, current['end']) + '!')

    if current['end'] == nxt['start']:
        color_id = ''
        try:
            color_id = current['colorId']
        except Exception:
            color_id = 'None'

        return join(
            colored_text('Ends in'),
            formatdd(now, current['end']) + colored_text('.'),
            colored_text('After this'),
            get_color_from_id(color_id, summary(nxt['summary'])),
            location(nxt['location'])
        )

    color_id = ''
    try:
        color_id = nxt['colorId']
    except Exception:
        color_id = 'None'

    return join(
        colored_text('Ends in'),
        formatdd(now, current['end']) + colored_text('.'),
        colored_text('After this'),
        get_color_from_id(color_id, summary(nxt['summary'])),
        location(nxt['location']),
        colored_text('After a break of'),
        formatdd(current['end'], nxt['start'])
    )


def activate_course(event):
    course = next(
        (course for course in courses
         if course.info['title'].lower() in event['summary'].lower()),
        None
    )

    if not course:
        return

    courses.current = course


def get_color_from_id(id, text):
    """
    Get color from id and text to colorize.

    Args:
        - id (int): color id (default: None)
        - text (str): text to colorize

    Returns:
        - str: colorized text
    """

    color = ''

    if not id:
        color = '#4f86f7'
    if id == '1':
        color = '#dcd0ff'
    if id == '2':
        color = '#bcb88a'
    if id == '3':
        color = '#6f2da8'
    if id == '4':
        color = '#fc8eac'
    if id == '5':
        color = '#ffe135'
    if id == '6':
        color = '#f28500'
    if id == '8':
        color = '#251607'
    if id == '9':
        color = '#326872'
    if id == '10':
        color = '#626e60'
    if id == '11':
        color = '#ff6347'

    return colored_text(text, color)


def main():
    """ Main function, which runs the program. """

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
        """
        Get events from the calendar and return them as a list of dicts.

        Args:
            - calendar (str): The calendar to get events from.

        Returns:
            - list: A list of dicts containing the events.
        """

        events_result = service.events().list(
            calendarId=calendar,
            timeMin=morning.isoformat(),
            timeMax=evening.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        try:
            return [
                {
                    'summary': event['summary'],
                    'location': event.get('location', None),
                    'colorId': event['colorId'],
                    'start': parse(event['start']['dateTime']),
                    'end': parse(event['end']['dateTime'])
                }
                for event in events
                if 'dateTime' in event['start']
            ]
        except Exception:
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

    events = get_events(courses.calendar_id)
    print('Done')

    DELAY = 60

    def print_message():
        """ Print the message. """

        now = datetime.datetime.now(tz=TZ)
        print(text(events, now))
        if now < evening:
            scheduler.enter(DELAY, 1, print_message)

    for event in events:
        # absolute entry, priority 1
        scheduler.enterabs(event['start'].timestamp(),
                           1, activate_course, argument=(event, ))

    # Immediate, priority 1
    scheduler.enter(0, 1, print_message)
    scheduler.run()


def wait_for_internet_connection(url, timeout=1):
    """
    Wait for internet connection to be available

    Args:
        - url (str): url to test
        - timeout (int): timeout in seconds to wait for connection to begin
            available (default: 1)

    Returns:
        - bool: True if connection is available, otherwise, keep trying
    """

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
