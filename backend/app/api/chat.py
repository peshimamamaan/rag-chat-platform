from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.chat import ChatSession
from app.services.chat_service import chat_with_gemini

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    session_id: int
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    session = db.get(ChatSession, payload.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    reply = chat_with_gemini(
        db=db,
        session_id=payload.session_id,
        user_message=payload.message
    )

    return {"reply": reply}