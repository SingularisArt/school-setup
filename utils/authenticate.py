import os
import pickle
import sys
from typing import Tuple

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def authenticate(
    type: str,
    scopes: Tuple[str],
    credentials_location: str,
) -> "build":
    print("Authenticating")
    SCOPES = scopes
    pickle_location = credentials_location.replace("json", "pickle")

    creds = None
    if os.path.exists(pickle_location):
        with open(pickle_location, "rb") as token:
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
                credentials_location,
                SCOPES,
            )
            creds = flow.run_local_server(port=0)
        with open(pickle_location, "wb") as token:
            pickle.dump(creds, token)

    service = build(type, "v3", credentials=creds)
    return service
