import requests
from app.core.config import settings

def create_connect_session(user_id: str):
    url = f"{settings.NANGO_HOST}/connect/sessions"

    payload = {
        "end_user": {
            "id": user_id
        },
        "allowed_integrations": ["google-drive"]
    }

    headers = {
        "Authorization": f"Bearer {settings.NANGO_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)

    if not response.ok:
        raise Exception(
            f"Nango error {response.status_code}: {response.text}"
        )

    return response.json()
