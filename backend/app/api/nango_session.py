from fastapi import APIRouter
import os
import requests
from app.core.config import settings

router = APIRouter()

NANGO_SECRET_KEY = settings.NANGO_SECRET_KEY
print("NANGO_SECRET_KEY:", NANGO_SECRET_KEY)

@router.post("/api/nango/session")
def create_nango_session():
    payload = {
        "end_user": {
            "id": "chat-user"
        }
    }

    headers = {
        "Authorization": f"Bearer {NANGO_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    r = requests.post(
        "https://api.nango.dev/connect/sessions",
        json=payload,
        headers=headers
    )

    return r.json()
