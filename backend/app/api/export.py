from fastapi import APIRouter, HTTPException, Response
from app.schemas.export import ExportRequest
from app.services.export_service import (
    generate_txt,
    generate_docx,
    generate_pdf,
)

router = APIRouter(prefix="/export", tags=["Export"])


@router.post("/response")
def export_response(payload: ExportRequest):
    if payload.format == "txt":
        file_bytes = generate_txt(payload.content)
        media_type = "text/plain"
        filename = "response.txt"

    elif payload.format == "docx":
        file_bytes = generate_docx(payload.content)
        media_type = (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        filename = "response.docx"

    elif payload.format == "pdf":
        file_bytes = generate_pdf(payload.content)
        media_type = "application/pdf"
        filename = "response.pdf"

    else:
        raise HTTPException(status_code=400, detail="Invalid format")

    return Response(
        content=file_bytes,
        media_type=media_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )
