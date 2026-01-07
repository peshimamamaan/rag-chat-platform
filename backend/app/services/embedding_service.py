from google import genai
from app.core.config import settings
from typing import List

client = genai.Client(api_key=settings.GEMINI_API_KEY)

EMBEDDING_MODEL = "models/text-embedding-004"

def embed_text(text: str) -> List[float]:
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )
    # 
    embeddings = response.embeddings
    if embeddings is None or len(embeddings) == 0:
        raise RuntimeError("Embedding service returned no embeddings")

    values = embeddings[0].values
    if values is None:
        raise RuntimeError("Embedding values are None")

    # ✅ Explicitly return a real list[float]
    return list(values)