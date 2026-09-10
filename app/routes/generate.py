import os
import json
import base64
from google.oauth2 import service_account


def get_genai_client():
    creds_b64 = os.environ.get("GOOGLE_CREDENTIALS_B64")

    if creds_b64:
        # Running somewhere without ambient GCP identity (e.g. Vercel) —
        # decode the service account key from the env var instead.
        creds_json = base64.b64decode(creds_b64).decode("utf-8")
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(creds_json),
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        return genai.Client(
            vertexai=True,
            project=Config.PROJECT_ID,
            location=Config.LOCATION,
            credentials=credentials,
        )

    # Running inside GCP (Cloud Shell, Cloud Run) — use ambient credentials.
    return genai.Client(vertexai=True, project=Config.PROJECT_ID, location=Config.LOCATION)