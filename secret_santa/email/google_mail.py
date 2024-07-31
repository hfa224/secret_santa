import base64
from email.message import EmailMessage


import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def gmail_send_message():
  """Create and send an email message
  Print the returned  message id
  Returns: Message object, including message id

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\Repos\secret-santa\instance\credentials.json"
  #creds, _ = google.auth.default()

  
  flow = InstalledAppFlow.from_client_secrets_file(
        '../instance/credentials.json', SCOPES)
  creds = flow.run_local_server(port=0)

  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    message.set_content("This is automated draft mail")

    message["To"] = "helenffionadams@gmail.com"
    message["From"] = "testingsanta3@gmail.com"
    message["Subject"] = "Automated draft"

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message


if __name__ == "__main__":
  gmail_send_message()