import requests
from app.core.config import settings

NANGO_INTEGRATION_KEY = "google-drive"
NANGO_BASE = "https://api.nango.dev"

def list_drive_files(connection_id: str):
    url = "https://api.nango.dev/proxy/drive/v3/files"

    headers = {
        "Authorization": f"Bearer {settings.NANGO_SECRET_KEY}",
        "Connection-Id": connection_id,
        "provider-config-key": NANGO_INTEGRATION_KEY,
    }

    params = {
        "pageSize": 20,
        "fields": "files(id,name,mimeType)"
    }

    response = requests.get(url, headers=headers, params=params)

    if not response.ok:
        raise Exception(
            f"Drive error {response.status_code}: {response.text}"
        )

    return response.json()

def download_drive_file(connection_id: str, file_id: str) -> bytes:
    url = f"{NANGO_BASE}/proxy/drive/v3/files/{file_id}?alt=media"

    headers = {
        "Authorization": f"Bearer {settings.NANGO_SECRET_KEY}",
        "provider-config-key": "google-drive",
        "connection-id": connection_id
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Drive download error: {response.text}")

    return response.content