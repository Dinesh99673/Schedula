from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timezone
import os, base64
from dotenv import load_dotenv
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_JSON_PATH = './service.json'
CALENDAR_ID = os.getenv("CALENDAR_ID")  # Share calendar with service account


# Decode and write only if not already present
if not os.path.exists(SERVICE_JSON_PATH):
    service_json_data = base64.b64decode(os.getenv("SERVICE_ACCOUNT_JSON_BASE64")).decode()
    with open(SERVICE_JSON_PATH, "w") as f:
        f.write(service_json_data)

credentials = service_account.Credentials.from_service_account_file(SERVICE_JSON_PATH, scopes=SCOPES)

service = build('calendar', 'v3', credentials=credentials)

# Define daily fixed slot times (hours only, no date)
DAILY_SLOT_TIMES = [
    {"start": "14:00", "end": "14:30"},
    {"start": "15:00", "end": "15:30"},
    {"start": "16:00", "end": "16:30"},
    {"start": "17:00", "end": "17:30"},
]

def get_slots_for_date(date_str):
    """Returns available datetime slots for a specific date (YYYY-MM-DD)."""
    available = []
    for slot in DAILY_SLOT_TIMES:
        start_iso = f"{date_str}T{slot['start']}:00+05:30"
        end_iso = f"{date_str}T{slot['end']}:00+05:30"

        if check_availability(start_iso, end_iso):
            available.append({"start": start_iso, "end": end_iso})

    return available

def book_event(title, start_time, end_time):
    event = {
        'summary': title,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
    }
    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return created_event

def check_availability(start_time, end_time):
    # Convert to ISO 8601 with timezone
    start_time_iso = datetime.fromisoformat(start_time).astimezone(timezone.utc).isoformat()
    end_time_iso = datetime.fromisoformat(end_time).astimezone(timezone.utc).isoformat()

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_time_iso,
        timeMax=end_time_iso,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return len(events.get('items', [])) == 0
