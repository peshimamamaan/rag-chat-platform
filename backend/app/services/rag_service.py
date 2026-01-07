from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.document import DocumentChunk
from app.models.chat import Message
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
    session_id: int,
    question: str,
    document_id: int | None
) -> str:
    user_msg = Message(
        session_id=session_id,
        role="user",
        content=question
    )
    db.add(user_msg)
    db.commit()

    chunks = retrieve_relevant_chunks(db, question, document_id)

    if not chunks:
        assistant_reply = "I don't know based on the provided documents."
    else:
        # 5. Build Prompt and Call AI
        prompt = build_rag_prompt(chunks, question)
        res = generate_response(prompt)
        assistant_reply = res if res is not None else "I don't know based on the provided documents."

    # 6. Save Assistant Message to DB
    assistant_msg = Message(
        session_id=session_id,
        role="assistant",
        content=assistant_reply
    )
    db.add(assistant_msg)
    db.commit()

    return assistant_reply