"""OAuth authentication for the Gmail API."""

from pathlib import Path

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Request read-only access to the Gmail account.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
]


# Resolve paths relative to the project, not the terminal directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"
TOKEN_FILE = PROJECT_ROOT / "token.json"


def get_credentials() -> Credentials:
    """Load existing OAuth credentials or authorize the user."""

    if not CREDENTIALS_FILE.is_file():
        raise FileNotFoundError(f"Missing OAuth client credentials: {CREDENTIALS_FILE}")

    creds = None

    # Reuse a previously authorized token if it exists.
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if creds and creds.valid:
        return creds

    # Refresh an expired access token when possible.
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except RefreshError:
            # Reauthorize if the refresh token is no longer valid.
            creds = None

    # Start the browser authorization flow if necessary.
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
        creds = flow.run_local_server(port=0)

    # Save credentials for subsequent CLI executions.
    TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    TOKEN_FILE.chmod(0o600)

    return creds
