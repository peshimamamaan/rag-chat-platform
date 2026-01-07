from sqlalchemy.orm import Session
from app.models.chat import Message
from app.services.gemini import generate_response

SYSTEM_PROMPT = (
    "You are a helpful, concise assistant. "
    "Answer clearly and accurately."
)

def build_prompt(messages: list[Message]) -> str:
    """
    Convert message history into a single prompt
    """
    prompt = SYSTEM_PROMPT + "\n\n"

    for msg in messages:
        if msg.role == "user":
            prompt += f"User: {msg.content}\n"
        else:
            prompt += f"Assistant: {msg.content}\n"

    prompt += "Assistant:"
    return prompt


def chat_with_gemini(
    db: Session,
    session_id: int,
    user_message: str
) -> str:
    # 1️⃣ Save user message
    user_msg = Message(
        session_id=session_id,
        role="user",
        content=user_message
    )
    db.add(user_msg)
    db.commit()

    # 2️⃣ Fetch full history
    history = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.created_at)
        .all()
    )

    # 3️⃣ Build prompt
    prompt = build_prompt(history)

    # 4️⃣ Gemini call
    assistant_reply = generate_response(prompt)

    # 5️⃣ Save assistant message
    assistant_msg = Message(
        session_id=session_id,
        role="assistant",
        content=assistant_reply
    )
    db.add(assistant_msg)
    db.commit()

    return assistant_reply
