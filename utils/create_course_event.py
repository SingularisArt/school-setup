import datetime

import config
import utils


def create_course_event(info):
    if info["type"].lower() == "online":
        return

    service = utils.authenticate(
        "calendar",
        ["https://www.googleapis.com/auth/calendar"],
        "credentials/calendar.json",
    )

    start_date = datetime.datetime.strptime(
        info["start-date"], config.date_format
    ).strftime("%Y-%m-%d")

    end_date = datetime.datetime.strptime(
        info["end-date"], config.date_format
    ).strftime("%Y%m%d")

    start_time = info["start-time"]
    end_time = info["end-time"]

    calendar_event = {
        "summary": info["short"],
        "location": info["location"],
        "start": {
            "dateTime": f"{start_date}T{start_time}",
            "timeZone": "America/Los_Angeles",
        },
        "end": {
            "dateTime": f"{start_date}T{end_time}",
            "timeZone": "America/Los_Angeles",
        },
        "recurrence": [
            f"RRULE:FREQ=WEEKLY;BYDAY={info['days']};UNTIL={end_date}",
        ],
    }

    service.events().insert(
        calendarId=config.calendar_id,
        body=calendar_event,
    ).execute()
