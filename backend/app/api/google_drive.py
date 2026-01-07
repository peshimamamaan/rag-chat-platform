from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.google_drive import list_drive_files, download_drive_file
from app.services.document_parser import parse_text
from app.models.document import Document
from app.schemas.drive import DriveImportRequest

router = APIRouter(prefix="/drive", tags=["Google Drive"])

@router.get("/files")
def get_drive_files(connection_id: str):
    return list_drive_files(connection_id)

@router.post("/import")
def import_drive_file(
    payload: DriveImportRequest,
    db: Session = Depends(get_db)
):
    raw_bytes = download_drive_file(
        payload.connection_id, 
        payload.file_id
    )
    content = parse_text(raw_bytes, payload.file_name)

    document = Document(
        name=payload.file_name,
        content=content
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "document_id": document.id,
        "message": "Document imported successfully"
    }