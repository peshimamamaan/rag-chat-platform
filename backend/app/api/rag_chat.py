from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.api.deps import get_db
from app.services.rag_service import rag_answer

router = APIRouter(prefix="/rag", tags=["RAG"])

class RAGRequest(BaseModel):
    session_id: int
    question: str
    document_id: Optional[int] = None

class RAGResponse(BaseModel):
    answer: str

@router.post("/ask", response_model=RAGResponse)
def ask_rag(payload: RAGRequest, db: Session = Depends(get_db)):
    doc_id = payload.document_id if payload.document_id is not None else 0
    answer = rag_answer(db=db, session_id=payload.session_id, question=payload.question, document_id=doc_id)
    return {"answer": answer}