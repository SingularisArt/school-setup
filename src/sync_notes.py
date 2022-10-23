#!/usr/bin/env python3

import os.path
import pickle
import sys

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from RofiLessonManager import utils as utils
from RofiLessonManager.courses import Courses as Courses


def authenticate():
    """
    Authenticates the user to access the google drive api.

    Returns:
        - googleapiclient.discovery.build
    """

    print("Authenticating")
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("credentials/sync.pickle"):
        with open("credentials/sync.pickle", "rb") as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
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
                "credentials/sync.json",
                SCOPES,
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("credentials/sync.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("drive", "v3", credentials=creds)
    return service


def main():
    courses = Courses()
    current = courses.current
    index = 0

    service = authenticate()

    for x, course in enumerate(courses):
        if course.name == current:
            index = x

        courses.current = course
        lectures = course.lectures

        r = lectures.parse_range_string("all")
        lectures.update_lectures_in_master(r)
        lectures.compile_master()

        try:
            file_metadata = {
                "name": "Notes",
                "parents": [course.info["folder"]],
            }

            media = MediaFileUpload(
                f"{course.path}/master.pdf",
                mimetype="application/pdf",
            )

            service.files().create(
                body=file_metadata, media_body=media, fields="id"
            ).execute()
        except HttpError:
            utils.rofi.msg(
                f"Failed to sync notes for course {course.info['name']}",
                err=True,
            )

            utils.rofi.msg(f"Synced notes for course {course.info['name']}")

    courses.current = courses[index]
