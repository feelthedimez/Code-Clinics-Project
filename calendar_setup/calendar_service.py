from __future__ import print_function
from datetime import datetime, timedelta
import pickle
import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pytz

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_service():
    """This function sets up the Google calendar API, and it returns the calendar 
    service."""
    
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_path = f"{sys.path[0]}/creds/token.pickle"
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            cred_path = f"{sys.path[0]}/creds/credentials.json"
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def get_events_results(calendar_id=None):
    """This function returns a list of calendar events results from the calendar
    service."""

    service = get_service()

    start, end = get_time_constraints()
    if calendar_id != None:
        events_results = service.events().list(calendarId=calendar_id,
                    timeMin=start, 
                    timeMax=end, 
                    singleEvents=True,
                    orderBy="startTime").execute()
    else:
        events_results = service.events().list(calendarId='primary',
                    timeMin=start, 
                    timeMax=end, 
                    singleEvents=True,
                    orderBy="startTime").execute()
    
    return events_results


def get_time_constraints(prompt_days=None): 
    """This function returns the start and end times for the calendar timeMin
    and timeMax."""

    if prompt_days == None:
        prompt_days = 7

    now = datetime.now(pytz.timezone("Africa/Cairo"))
    end = now + timedelta(days=prompt_days)
    start = now.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
    end = end.strftime("%Y-%m-%dT%H:%M:%S") + "Z"

    return start, end