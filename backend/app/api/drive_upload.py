from fastapi import APIRouter, Query
from app.services.google_drive_upload import upload_file_to_drive

router = APIRouter(prefix="/drive", tags=["Google Drive"])


@router.post("/upload")
def upload_to_drive(
    connection_id: str = Query(...),
    filename: str = Query(...),
    content: str = Query(...),
):
    """
    TEMP endpoint to verify upload works.
    We'll replace this with export integration next.
    """

    result = upload_file_to_drive(
        connection_id=connection_id,
        filename=filename,
        content_bytes=content.encode("utf-8"),
        mime_type="text/plain",
    )

    return {
        "file_id": result.get("id"),
        "name": result.get("name"),
    }
