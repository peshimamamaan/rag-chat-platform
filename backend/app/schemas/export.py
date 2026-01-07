from pydantic import BaseModel
from typing import Literal, Optional


class ExportRequest(BaseModel):
    content: str
    format: Literal["txt", "docx", "pdf"]
    filename: Optional[str] = None
    connection_id: str
