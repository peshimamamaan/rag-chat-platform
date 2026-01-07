from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.services.document_parser import parse_document

router = APIRouter(prefix="/documents", tags=["Documents"])



@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename or not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF and TXT supported")

    try:
        text = parse_document(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not text.strip():
        raise HTTPException(status_code=400, detail="Document is empty")

    document = Document(
        name=file.filename,
        content=text)
    db.add(document)
    db.commit()
    db.refresh(document)

    # ⚠️ We are NOT chunking yet (Step 6)
    # Raw text stays in memory for now

    return document