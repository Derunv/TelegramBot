# import os.path
# from googleapiclient.discovery import build
# from google.oauth2 import service_account
#
# SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "credentials.json")
#
# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES
# )
#
# # The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = "1y0of1ZXXF-JIHv2c8XrgvwJbRQcDGLSj58rXaCVSs6o"
# SAMPLE_RANGE_NAME = "A"
#
#
# service = build("sheets", "v4", credentials=credentials)
# sheet = service.spreadsheets()
# result = (
#     sheet.values()
#     .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
#     .execute()
# )
#
# print(result)

import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Google Sheets API setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "credentials.json")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1y0of1ZXXF-JIHv2c8XrgvwJbRQcDGLSj58rXaCVSs6o"

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
sheets_instance = build("sheets", "v4", credentials=creds)
range_name = "A!A:F"


# Google Sheets append data
def append_data_to_sheet():

    list = [["valuea1", "hgfgh", "fghfhfgh"]]
    body = {"majorDimension": "ROWS", "values": list}

    sheets_instance.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body,
    ).execute()


def get_data_from_file():
    result = (
        sheets_instance.spreadsheets()
        .values()
        .get(spreadsheetId=SPREADSHEET_ID, range=range_name)
        .execute()
    )

    values = result.get("values", [])
    return values


async def check_user_registered(user_id) -> bool:
    sheet_data = await get_data_from_file()
    for row in sheet_data:
        if row[0] == str(user_id):
            return True
    return False


async def get_all_registered_users():
    sheet_data = await get_data_from_file()
    return sheet_data[1:]


print(append_data_to_sheet())
