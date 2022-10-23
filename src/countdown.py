#!/usr/bin/python3

import datetime
import os
import os.path
import pickle
import re
import sched
import sys
import time
import urllib.request

from dateutil.parser import parse
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pytz

from RofiLessonManager.courses import Courses as Courses
import RofiLessonManager.utils as utils
import config

courses = Courses()


def authenticate():
    print("Authenticating")

    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    creds = None
    if os.path.exists("credentials/calendar.pickle"):
        with open("credentials/calendar.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError as e:
                print(e)
                sys.exit()
        else:
            print("Need to allow access")
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/calendar.json",
                SCOPES,
            )
            creds = flow.run_local_server(port=0)
        with open("credentials/calendar.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)
    return service


def text(events, now):
    current = next(
        (e for e in events if e["start"] < now and now < e["end"]),
        None,
    )

    period = utils.colored_text(".")
    if not current:
        nxt = next((e for e in events if now <= e["start"]), None)
        if nxt:
            print(utils.format_date_and_time(now, nxt["start"]))
            return utils.join(
                utils.colored_text(nxt["type"]),
                utils.summary(nxt["summary"]),
                utils.colored_text("starts in"),
                utils.format_date_and_time(now, nxt["start"]),
                utils.location(nxt["location"]),
                "   ",
                utils.format_time(nxt["start"]),
            )
        return ""
    nxt = next((e for e in events if e["start"] >= current["end"]), None)
    if not nxt:
        return utils.join(
            utils.colored_text(current["type"]),
            utils.colored_text("Ends in"),
            utils.format_date_and_time(now, current["end"]) + "!",
            "   ",
            utils.format_time(current["end"]),
        )

    if current["end"] == nxt["start"]:
        return utils.join(
            utils.colored_text(nxt["type"]),
            utils.colored_text("Ends in"),
            utils.format_date_and_time(now, current["end"]) + period,
            utils.colored_text("Next:"),
            utils.summary(nxt["summary"]),
            utils.location(nxt["location"]),
            "   ",
            utils.format_time(nxt["start"]),
        )

    return utils.join(
        utils.colored_text(nxt["type"]),
        utils.colored_text("Ends in"),
        utils.format_date_and_time(now, current["end"]) + period,
        utils.colored_text("Next:"),
        utils.summary(nxt["summary"]),
        utils.location(nxt["location"]),
        utils.colored_text("after a"),
        utils.format_date_and_time(current["end"], nxt["start"]),
        utils.colored_text("break."),
        "   ",
        utils.format_time(current["end"]),
    )


def activate_course(event):
    course = next(
        (
            course
            for course in courses
            if course.info["title"].lower() in event["summary"].lower()
        ),
        None,
    )

    if not course:
        return

    if course.info["title"] == event["summary"]:
        courses.current = course


def main():
    scheduler = sched.scheduler(time.time, time.sleep)

    print("Initializing")

    TZ = ""

    if "TZ" in os.environ:
        TZ = pytz.timezone(os.environ["TZ"])
    else:
        print("Warning: TZ environ variable not set")
        return

    service = authenticate()

    print("Authenticated")

    now = datetime.datetime.now(tz=TZ)

    morning = now.replace(hour=6, minute=0, microsecond=0)
    evening = now.replace(hour=23, minute=59, microsecond=0)

    print("Searching for events")

    def get_events(calendar):
        events_result = (
            service.events()
            .list(
                calendarId=calendar,
                timeMin=morning.isoformat(),
                timeMax=evening.isoformat(),
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        new_events = []

        for event in events:
            regex = r"^([ a-zA-Z0-9]+): (CLASS|LAB)$"

            try:
                parsed_event = re.search(regex, event["summary"])

                if not parsed_event:
                    return

                summary = parsed_event.group(1)
                type = parsed_event.group(2).title()

                if "dateTime" in event["start"]:
                    event_dict = {
                        "summary": summary,
                        "location": event.get("location", None),
                        "start": parse(event["start"]["dateTime"]),
                        "end": parse(event["end"]["dateTime"]),
                        "type": type,
                    }

                    new_events.append(event_dict)
            except Exception:
                pass

        return new_events

    events = get_events(config.calendar_id)
    print("Done")
    time.sleep(1)
    print("")

    DELAY = 60

    def print_message():
        now = datetime.datetime.now(tz=TZ)
        print(text(events, now))
        if now < evening:
            scheduler.enter(DELAY, 1, print_message)

    for event in events:
        scheduler.enterabs(
            event["start"].timestamp(), 1, activate_course, argument=(event,)
        )

    scheduler.enter(0, 1, print_message)
    scheduler.run()


def check_internet(host="http://google.com"):
    """
    Checks if connected to the internet.

    Args:
        - host (str): Checks if connected (Default: https://google.com).
    """

    while True:
        try:
            urllib.request.urlopen(host)
            break
        except Exception:
            pass


if __name__ == "__main__":
    os.chdir(sys.path[0])
    print("Waiting for connection")
    check_internet()
    main()
