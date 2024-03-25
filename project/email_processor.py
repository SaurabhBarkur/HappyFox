import os
import sys
import django
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime

#Initialize
project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), 'project'))
sys.path.append(project_directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from gmail.models import Email
from gmail.apply_rules import apply_rules

#SCOPES = ['https://mail.google.com/']
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())


service = build('gmail', 'v1', credentials=creds)

def fetch_email(service):
    result = service.users().messages().list(userId='me').execute()
    messages = result.get('messages')
    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        internal_date_seconds = int(txt["internalDate"]) / 1000
        email_date= datetime.utcfromtimestamp(internal_date_seconds)
        message_id = int(msg.get("id"),16)
        thread_id = int(msg.get("threadId"),16)
        email_data = txt.get("payload").get("headers")
        for values in email_data:
            name = values.get("name")
            if name == "From":
                email_from = values.get("value")
            elif name == "To":
                email_sender = values.get("value")
            elif name == "Subject":
                email_subject = values.get("value")
        value = txt.get("payload").get("body").get("size")
        if value > 0:
            res_data = base64.urlsafe_b64decode(txt["payload"]["body"].get("data")).decode("utf-8")
        else:
            res_data = ""
            for p in txt["payload"]["parts"]:
                data = base64.urlsafe_b64decode(p["body"].get("data","")).decode("utf-8")
                res_data = res_data + data
        email, _ = Email.objects.get_or_create(email_id=message_id, thread_id=thread_id, email_from=email_from,email_to=email_sender,date=email_date,subject=email_subject,body=res_data)

if __name__ == "__main__":
    email_count = Email.objects.all().count()
    if email_count < 1:
        fetch_email(service=service)
    else:
        apply_rules()