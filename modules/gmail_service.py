"""
Gmail service management module.
"""
import os
import pickle
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GmailService:
    """Gmail service handler."""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    
    def __init__(self):
        self.service = self._get_service()
        self.user_email = self._get_user_email()
    
    def _get_service(self):
        """Get or create Gmail API service."""
        creds = None
        token_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'token.pickle')
        credentials_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials.json')

        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)
    
    def _get_user_email(self):
        """Get authenticated user's email address."""
        return self.service.users().getProfile(userId='me').execute()['emailAddress']
    
    def create_message(self, to, subject, message_text, cc=None):
        """Create a message for an email."""
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = self.user_email
        message['subject'] = subject
        if cc:
            message['cc'] = cc
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    
    def send_message(self, message):
        """Send an email message."""
        return self.service.users().messages().send(userId='me', body=message).execute()
