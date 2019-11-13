from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/presentations']

def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    create_presentation('hello', creds)

def create_presentation(title, creds):
    slides_service = build('slides', 'v1', credentials=creds)
    # [START slides_create_presentation]
    body = {
        'title': title
    }
    presentation = slides_service.presentations() \
        .create(body=body).execute()
    print('Created presentation with ID: {0}'.format(
        presentation.get('presentationId')))
    # [END slides_create_presentation]
    return presentation

if __name__ == '__main__':
    main()