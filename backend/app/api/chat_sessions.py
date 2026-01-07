from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.chat import ChatSession
from app.schemas.chat import chatSessionCreate, chatSessionResponse

router = APIRouter(prefix="/sessions", tags=["Chat Sessions"])

@router.post("", response_model=chatSessionResponse)
def create_session(payload: chatSessionCreate, db: Session = Depends(get_db)):
    session = ChatSession(title=payload.title)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@router.get("", response_model=list[chatSessionResponse])
def list_sessions(db: Session = Depends(get_db)):
    sessions = db.query(ChatSession).order_by(ChatSession.created_at.desc()).all()
    return sessions

@router.delete("/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    session = db.get(ChatSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    db.delete(session)
    db.commit()
    return {"status": "Chat session deleted"}