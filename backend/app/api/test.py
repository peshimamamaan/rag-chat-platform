from fastapi import APIRouter
from app.services.gemini import generate_response
from pydantic import BaseModel

router = APIRouter(prefix="/test", tags=["Test"])

class GeminiRequest(BaseModel):
    prompt: str

# @router.post("/test-gemini")
# def test(prompt: str):
#     return {"reply": generate_response(prompt)}

@router.post("/gemini")
def test_gemini(data: GeminiRequest):
    reply = generate_response(data.prompt)
    return {"reply": reply}