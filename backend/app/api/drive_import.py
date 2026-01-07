from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.api.deps import get_db
from app.services.drive_import_service import import_drive_file

router = APIRouter(prefix="/drive", tags=["Google Drive"])

class DriveImportRequest(BaseModel):
    file_id: str
    file_name: str
    connection_id: str


@router.post("/import")
def import_from_drive(
    payload: DriveImportRequest,
    db: Session = Depends(get_db),
):
    document = import_drive_file(
        db=db,
        file_id=payload.file_id,
        connection_id=payload.connection_id,
    )

    return {
        "id": document.id,
        "title": document.title,
        "status": "imported",
    }
