from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.chat import Message, ChatSession
from app.schemas.message import MessageCreate, MessageResponse

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("", response_model=MessageResponse)
def create_message(payload: MessageCreate, db: Session = Depends(get_db)):
    session = db.get(ChatSession, payload.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    msg = Message(
        session_id=payload.session_id,
        role=payload.role,
        content=payload.content
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

@router.get("/{session_id}", response_model=list[MessageResponse])
def get_messages(session_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.created_at)
        .all()
    )
