import json
import requests
import io
from fastapi import APIRouter, HTTPException
from fpdf import FPDF
from app.schemas.export import ExportRequest
from app.core.config import settings

router = APIRouter(prefix="/export", tags=["Export"])

NANGO_PROXY_BASE = "https://api.nango.dev/proxy"

def create_pdf_bytes(text_content: str) -> bytes:
    """Helper to convert string content into PDF bytes"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    
    # multi_cell handles line breaks automatically
    pdf.multi_cell(0, 10, text_content)
    
    # Output to bytes
    return pdf.output()

@router.post("/drive")
def export_to_drive(payload: ExportRequest):
    if not payload.connection_id:
        raise HTTPException(status_code=400, detail="connection_id is required")

    # 1. Determine Format Logic
    is_pdf = (payload.format or "").lower() == "pdf"
    
    if is_pdf:
        mime_type = "application/pdf"
        # Ensure filename ends in .pdf
        filename = payload.filename or "rag_answer.pdf"
        if not filename.endswith(".pdf"):
            filename += ".pdf"
            
        # Generate PDF binary data
        try:
            file_data = create_pdf_bytes(payload.content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PDF Generation failed: {str(e)}")
            
    else:
        # Default to Text
        mime_type = "text/plain"
        filename = payload.filename or "rag_answer.txt"
        file_data = payload.content.encode("utf-8")

    # Common Headers
    headers = {
        "Authorization": f"Bearer {settings.NANGO_SECRET_KEY}",
        "provider-config-key": "google-drive",
        "connection-id": payload.connection_id,
        "X-Nango-Proxy-Base-Url": "https://www.googleapis.com"
    }

    # ======================================================================
    # STEP 1: Create Metadata
    # ======================================================================
    metadata_body = {
        "name": filename,
        "mimeType": mime_type
    }

    print(f"Step 1: Creating file metadata for {filename}...")
    meta_res = requests.post(
        f"{NANGO_PROXY_BASE}/drive/v3/files",
        headers=headers,
        json=metadata_body
    )

    if not meta_res.ok:
        raise HTTPException(status_code=500, detail=f"Metadata creation failed: {meta_res.text}")

    file_id = meta_res.json().get("id")

    # ======================================================================
    # STEP 2: Upload Content
    # ======================================================================
    upload_headers = headers.copy()
    upload_headers["Content-Type"] = mime_type

    print(f"Step 2: Uploading {len(file_data)} bytes to file ID {file_id}...")
    
    upload_res = requests.patch(
        f"{NANGO_PROXY_BASE}/upload/drive/v3/files/{file_id}?uploadType=media",
        headers=upload_headers,
        data=file_data  # Send the correct bytes (PDF or Text)
    )

    if not upload_res.ok:
        raise HTTPException(status_code=500, detail=f"Content upload failed: {upload_res.text}")

    return {
        "status": "success",
        "file_id": file_id,
        "link": f"https://drive.google.com/open?id={file_id}",
        "format": "pdf" if is_pdf else "txt"
    }