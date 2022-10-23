import os
import pickle
import sys

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def authenticate(type, scopes, credentials_location):
    print("Authenticating")
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = scopes
    pickle_location = credentials_location.replace("json", "pickle")

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(pickle_location):
        with open(pickle_location, "rb") as token:
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
                credentials_location,
                SCOPES,
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pickle_location, "wb") as token:
            pickle.dump(creds, token)

    service = build(type, "v3", credentials=creds)
    return service
