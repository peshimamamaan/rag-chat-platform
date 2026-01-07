import requests
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.config import settings
from app.models.document import Document

NANGO_PROXY_BASE = "https://api.nango.dev/proxy"


def import_drive_file(
    *,
    db: Session,
    connection_id: str,
    file_id: str,
):
    """
    Downloads a Google Drive file via Nango and saves it as a Document
    """

    headers = {
        "Authorization": f"Bearer {settings.NANGO_SECRET_KEY}",
        "provider-config-key": "google-drive",
        "connection-id": connection_id,
    }

    # Download file content
    res = requests.get(
        f"{NANGO_PROXY_BASE}/drive/v3/files/{file_id}?alt=media",
        headers=headers,
    )

    if not res.ok:
        raise HTTPException(
            status_code=500,
            detail=f"Drive download failed: {res.text}",
        )

    content = res.text

    if not content.strip():
        raise HTTPException(
            status_code=400,
            detail="Downloaded file is empty",
        )

    # Save document to DB
    document = Document(
        title=f"Drive File {file_id}",
        content=content,
        source="google-drive",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document
