print("✅ embeddings.py LOADED FROM:", __file__)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import cast

from app.api.deps import get_db
from app.models.document import Document, DocumentChunk
from app.services.chunking import chunk_text
from app.services.embedding_service import embed_text

router = APIRouter(prefix="/embeddings", tags=["Embeddings"])

print("embeddings router loaded")

@router.post("/document/{document_id}")
def embed_document(document_id: int, db: Session = Depends(get_db)):
    print("embed_document CALLED", document_id)
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if not document.content:
        raise HTTPException(status_code=400, detail="Document has no content")

    text = cast(str, document.content)

    chunks = chunk_text(text)

    for chunk in chunks:
        embedding = embed_text(chunk)
        print(len(embedding))
        db.add(DocumentChunk(
            document_id=document.id,
            content=chunk,
            embedding=embedding
        ))

    db.commit()

    return {
        "document_id": document.id,
        "chunks_created": len(chunks)
    }
