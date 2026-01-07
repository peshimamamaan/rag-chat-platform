import requests
import json
from app.core.config import settings


def upload_file_to_drive(
    connection_id: str,
    filename: str,
    content_bytes: bytes,
    mime_type: str,
):
    """
    Uploads a file to Google Drive using Nango proxy
    """

    url = f"{settings.NANGO_HOST}/proxy/upload/drive/v3/files?uploadType=media"

    headers = {
        "Authorization": f"Bearer {settings.NANGO_SECRET_KEY}",
        "Connection-Id": connection_id,
        "Provider-Config-Key": "google-drive",
        "Content-Type": mime_type,
        "X-Upload-Content-Type": mime_type
    }

    metadata = {
        "name": filename
    }

    files = {
        "metadata": (
            "metadata.json",
            json_dumps(metadata),
            "application/json; charset=UTF-8",
        ),
        "media": (
            filename,
            content_bytes,
            mime_type,
        ),
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code not in (200, 201):
        raise Exception(
            f"Google Drive upload failed: {response.status_code} {response.text}"
        )

    return response.json()


def json_dumps(obj):
    import json
    return json.dumps(obj)
