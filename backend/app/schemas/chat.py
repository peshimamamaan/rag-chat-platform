from pydantic import BaseModel
from datetime import datetime

class chatSessionCreate(BaseModel):
    title: str

class chatSessionResponse(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        from_attributes = True