import json

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

with open("credenciales.json") as f:
    credenciales_json = json.load(f)

flow = InstalledAppFlow.from_client_config(
    credenciales_json,
    scopes=SCOPES
)

creds = flow.run_local_server(port=0)
print(f"Refresh token: {creds.refresh_token}")
#"C:\Users\34699\Downloads\client_secret_300388750395-onsincledgpf5v2un2sp1m2e2vlt434l.apps.googleusercontent.com.json"