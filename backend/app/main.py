from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from app.api import chat_sessions, messages, chat, documents, embeddings, rag_chat, nango, google_drive, export, drive_upload, export_drive, nango_session

# print("Database URL:", settings.DATABASE_URL)
# print("Gemini API Key:", settings.GEMINI_API_KEY)

app = FastAPI(title="LLM RAG Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_sessions.router)
app.include_router(messages.router)
app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(embeddings.router)
app.include_router(rag_chat.router)
app.include_router(nango.router)
app.include_router(google_drive.router)
app.include_router(export.router)
app.include_router(drive_upload.router)
app.include_router(export_drive.router)
app.include_router(nango_session.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}