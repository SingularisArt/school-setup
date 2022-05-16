#!/usr/bin/python3

"""
This program gets the current events from Google Calendar and displays them.
You can use this script to create a polybar module because I use different
colors on different texts to work with polybar.

Example:

Ends in 25 minutes. After this, a break for 25 minutes. Then, Pre-Calculus II.
Ends in 25 minutes. After this, Pre-Calculus II!
Ends in 25 minutes.

Function authenticate:
    - src.calendar.authenticate

    Authenticate with Google Calendar API.

    Returns:
        - service (object): authenticated service

Function text:
    - src.calendar.text
    Generate text for the current events and the next events.

    Args:
        - events (list): list of events
        - now (datetime): current time

    Returns:
        - str: text to display

Function activate_course:
    Activate the current course.

    Args:
        - event (dict): event to activate

    Returns:
        - bool: True if the course was activated, otherwise, False

Function wait_for_internet_connection:
    - src.calendar.wait_for_internet_connection

    Wait for internet connection to be available

    Args:
        - url (str): url to test
        - timeout (int): timeout in seconds to wait for connection to begin
            available (default: 1)

    Returns:
        - bool: True if connection is available, otherwise, keep trying
"""

import pickle

import os
import os.path
import sys

import re

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
import RofiLessonManager.utils as utils

courses = Courses()


def authenticate():
    """
    Authenticate with Google Calendar API.

    Returns:
        - service (object): authenticated service
    """

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


def text(events, now):
    """
    Generate text for the current events and the next events.

    Args:
        - events (list): list of events
        - now (datetime): current time

    Returns:
        - str: text to display
    """

    current = next(
        (e for e in events if e['start'] < now and now < e['end']), None)

    study_or_not_1 = ''
    study_or_not_2 = ''

    if not current:
        nxt = next((e for e in events if now <= e['start']), None)
        print(nxt['summary'])
        study = re.search('(.+) Study', nxt['summary'])
        print(study.group(1))

        if nxt:
            color_id = ''
            try:
                color_id = nxt['colorId']
            except Exception:
                color_id = 'None'

            if not study:
                return utils.join(
                    utils.get_color_from_id(
                        color_id, utils.summary(nxt['summary'])),
                    utils.colored_text('starts in'),
                    utils.formatdd(now, nxt['start']),
                    utils.location(nxt['location'])
                )
            else:
                return utils.join(
                    utils.colored_text('Study'),
                    utils.get_color_from_id(
                        color_id, study.group(1)),
                    utils.colored_text('in'),
                    utils.formatdd(now, nxt['start']),
                )
        return ''

    study = re.search('(.+)Study(.+)', current['summary'])
    print(study)

    if not nxt:
        nxt = next((e for e in events if e['start'] >= current['end']), None)

        if not study:
            return utils.join(utils.colored_text('Ends in'),
                              utils.formatdd(now, current['end']) + '!')
        else:
            return utils.join(utils.colored_text('Stop studying ' +
                                                 utils.summary(
                                                     current['summary'])),
                              utils.formatdd(now, current['end']) + '!')

    if current['end'] == nxt['start']:
        color_id = ''
        try:
            color_id = current['colorId']
        except Exception:
            color_id = 'None'

        lines = [
            utils.colored_text(study_or_not_1),
            utils.formatdd(now, current['end']) + utils.colored_text('.'),
            utils.colored_text(study_or_not_2),
            utils.get_color_from_id(color_id,
                                    utils.summary(nxt['summary'])) + '.',
        ]

        if not study:
            study_or_not_1 = 'Ends in'
            study_or_not_2 = 'After this, '
            lines = utils.join(lines)
            return utils.join(
                lines,
                utils.location(nxt['location'])
            )
        else:
            study_or_not_1 = 'Stop studying'
            study_or_not_2 = 'Then, study'
            lines = utils.join(lines)
            return utils.join(
                lines,
                utils.location(nxt['location'])
            )

    color_id = ''
    try:
        color_id = nxt['colorId']
    except Exception:
        color_id = 'None'

    study_or_not_1 = ''
    study_or_not_2 = ''

    lines = [
        utils.colored_text(study_or_not_1),
        utils.formatdd(now, current['end']) + utils.colored_text('.'),
        utils.colored_text('After this, a break for'),
        utils.formatdd(current['end'], nxt['start']) + '.',
        utils.colored_text(study_or_not_2),
        utils.get_color_from_id(
            color_id, utils.summary(nxt['summary'])) + '.',
    ]

    if not study:
        study_or_not_1 = 'Ends in'
        study_or_not_2 = 'After this, '
        lines = utils.join(lines)
        return utils.join(
            lines,
            utils.location(nxt['location']),
        )
    else:
        study_or_not_1 = 'Stop studying'
        study_or_not_2 = 'Then, study'
        lines = utils.join(lines)
        return utils.join(
            lines,
            utils.location(nxt['location']),
        )


def activate_course(event):
    """
    Activate the current course.

    Args:
        - event (dict): event to activate

    Returns:
        - bool: True if the course was activated, otherwise, False
    """

    course = next(
        (course for course in courses
         if course.info['title'].lower() in event['summary'].lower()),
        None
    )

    if not course:
        return

    courses.current = course


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
