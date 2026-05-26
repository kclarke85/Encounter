from google_auth_oauthlib.flow import InstalledAppFlow  # ✅ This line was missing

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=64139)

