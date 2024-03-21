import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "credentials.json")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1y0of1ZXXF-JIHv2c8XrgvwJbRQcDGLSj58rXaCVSs6o"

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
sheets_instance = build("sheets", "v4", credentials=creds)
range_name = "A!A:F"


def append_data_to_sheet(data: list[list[str]]) -> None:
    body = {"majorDimension": "ROWS", "values": data}

    sheets_instance.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body,
    ).execute()
