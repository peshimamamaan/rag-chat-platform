from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.document import DocumentChunk
from app.services.embedding_service import embed_text
from app.services.gemini import generate_response

TOP_K = 5

def retrieve_relevant_chunks(
    db: Session,
    query: str,
    document_id: int | None,
    top_k: int = TOP_K,
) -> list[str]:
    query_embedding = embed_text(query)

    print("🔎 Query embedding length:", len(query_embedding))

    # sql = text("""
    #     SELECT content
    #     FROM document_chunks
    #     WHERE document_id = :document_id
    #     ORDER BY embedding <-> (:query_embedding)::vector
    #     LIMIT :top_k
    # """)

    # results = db.execute(
    #     sql,
    #     {
    #         "query_embedding": query_embedding,
    #         "document_id": document_id,
    #         "top_k": top_k,
    #     }
    # )

    # print("Retrieved chunks:", results)
    if document_id:
        sql = text("""
            SELECT content
            FROM document_chunks
            WHERE document_id = :document_id
            ORDER BY embedding <-> CAST(:query_embedding AS vector)
            LIMIT :top_k
        """)
        params = {
            "query_embedding": query_embedding,
            "top_k": top_k,
            "document_id": document_id,
        }
    else:
        sql = text("""
            SELECT content
            FROM document_chunks
            ORDER BY embedding <-> CAST(:query_embedding AS vector)
            LIMIT :top_k
        """)
        params = {
            "query_embedding": query_embedding,
            "top_k": top_k,
        }

    results = db.execute(sql, params).fetchall()
    return [row[0] for row in results]

SYSTEM_PROMPT = """
You are a question-answering assistant.

Answer the question using the information provided in the context.
You may summarize, paraphrase, and infer reasonable conclusions from the context.

Do not introduce facts that are not supported by the context.

If the context is completely unrelated to the question, say exactly:
"I don't know based on the provided documents."
"""

def build_rag_prompt(context_chunks: list[str], question: str) -> str:
    context = "\n\n".join(context_chunks)

    return f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}

Answer:
""".strip()


def rag_answer(
    db: Session,
    question: str,
    document_id: int | None
) -> str:
    chunks = retrieve_relevant_chunks(db, question, document_id)

    if not chunks:
        return "I don't know based on the provided documents."

    prompt = build_rag_prompt(chunks, question)
    response = generate_response(prompt)
    return response if response is not None else "I don't know based on the provided documents."