#!/usr/bin/python3

"""
This program gets the current events from Google Calendar and displays them.
You can use this script to create a polybar module because I use different
colors on different texts to work with polybar.

Examples:

Stop studying Pre-Calculus II in 39 minutes. After this, start College SS.
Stop studying Pre-Calculus II in 39 minutes. Then, take a break for 30 minutes.
    Then, start College SS.
Stop studying Pre-Calculus II in 39 minutes.
...

Function authenticate:
    - src.calendar.authenticate

    Authenticate with Google Calendar API.

    Returns:
        - service (object): authenticated service

Function get_color_id:
    - src.calendar.get_color_id

    Get the color id of the event.

    Args:
        - event (dict): event to get the color id

    Returns:
        - str: color id

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

TODO: Make this program also work on other things like:
    College Composition: Essay and the program will transform that into:

    Stop working on the College Composition Essay in 29 minutes.
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


def get_color_id(event):
    """
    Get the color id of the event.

    Args:
        - event (dict): event to get the color id

    Returns:
        - str: color id
    """

    color_id = ''
    try:
        color_id = event['colorId']
    except Exception:
        color_id = 'None'

    return color_id


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

    # Checking if there are no other events after the current one.
    ###########################################################################
    if not current:
        # Get the next event
        nxt = next((e for e in events if now <= e['start']), None)
        # Get the current class
        summary = nxt['summary']
        # Parse the current event to see if we are in a study session.
        study = re.search('(.+) Study', summary)

        if nxt:
            color_id = get_color_id(nxt)

            study_or_start_text = ''
            in_or_start = ''

            if study:
                study_or_start_text = 'Study'
                in_or_start = 'in'
            else:
                study_or_start_text = ''
                in_or_start = 'starts in'

            # Example output:
            # College Composition starts in 25 minutes in TCB 208
            # Study College Composition in 25 minutes
            return utils.join(
                utils.colored_text(study_or_start_text),
                utils.get_color_from_id(color_id, summary),
                utils.colored_text(in_or_start),
                utils.formatdd(now, nxt['start']),
                utils.location(nxt['location'])
            )
        return ''
    ###########################################################################

    # Parse the current event to see if we are in a study session.
    study = re.search('(.+) Study', current['summary'])
    # Get the next event
    nxt = next((e for e in events if e['start'] >= current['end']), None)

    ###########################################################################
    if not nxt:
        # Get the id for the color
        color_id = get_color_id(current)
        # Get the current class
        summary = current['summary']
        # Parse the current to see if we are in a study session
        study = re.search('(.+) Study', summary)

        # Check if we are in a study session
        if study:
            summary = study.group(1)
            start = utils.colored_text('Stop studying ') + \
                utils.get_color_from_id(color_id,
                                        summary) + \
                utils.colored_text(' in')
        # Check if we aren't in a study session
        else:
            start = utils.colored_text('Stop ') + utils.get_color_from_id(
                color_id, summary) + utils.colored_text(' in')

        return utils.join(
            start,
            utils.formatdd(now, current['end']),
            utils.location(current['location'])
        )
    ###########################################################################

    ###########################################################################
    if current['end'] == nxt['start']:
        # Get the id for the color
        current_id_color = get_color_id(current)
        next_color_id = get_color_id(nxt)
        # Get the current and next class name
        current_summary = utils.get_color_from_id(current_id_color,
                                                  current['summary'])
        next_summary = nxt['summary']
        # Parse the current and next event to see if we are in a study session.
        study_current = re.search('(.+) Study', current_summary)
        study_next = re.search('(.+) Study', next_summary)

        after = 'After this,'
        start = ''

        # If we are in a study session
        if study_current:
            current_summary = utils.get_color_from_id(current_id_color,
                                                      study_current.group(1))
            start = utils.colored_text('Stop studying ') + current_summary + \
                utils.colored_text(' in')
        # If we aren't in a study session
        else:
            start = current_summary + utils.colored_text(' ends in')
            start = utils.colored_text('Stop ') + current_summary + \
                utils.colored_text(' in')

        if study_next:
            next_summary = utils.get_color_from_id(next_color_id,
                                                   study_next.group(1))
            after += ' study'
        else:
            after += ' start'

        return utils.join(
            start,
            utils.formatdd(now, current['end']) + utils.colored_text('.'),
            utils.colored_text(after),
            utils.get_color_from_id(next_color_id, next_summary),
            utils.location(nxt['location'])
        )
    ###########################################################################

    # Get the id for the color
    current_id_color = get_color_id(current)
    next_id_color = get_color_id(nxt)
    color_id = get_color_id(nxt)

    ###########################################################################
    current_summary = utils.get_color_from_id(current_id_color,
                                              current['summary'])
    next_summary = utils.get_color_from_id(next_id_color, nxt['summary'])
    current_study = re.search('(.+) Study', current_summary)
    next_study = re.search('(.+) Study', next_summary)

    start = ''
    after = ''

    # Check if we are in a study session
    if current_study:
        current_summary = utils.get_color_from_id(color_id, study.group(1))
        start = utils.colored_text('Stop studying ') + current_summary + \
            utils.colored_text(' in')
    # Check if we aren't in a study session
    else:
        start = current_summary + utils.colored_text(' ends in')

    if next_study:
        next_summary = utils.get_color_from_id(next_id_color,
                                               next_study.group(1))
        after = 'Then, study'
    else:
        after = 'Then, start'

    return utils.join(
        start,
        utils.formatdd(now, current['end']) + utils.colored_text('.'),
        utils.colored_text('Then, take a break for'),
        utils.formatdd(current['end'], nxt['start']) + utils.colored_text('.'),
        utils.colored_text(after),
        next_summary,
        utils.location(nxt['location']),
    )
    ###########################################################################


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
