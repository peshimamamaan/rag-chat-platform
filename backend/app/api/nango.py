from fastapi import APIRouter
from app.services.nango_connect import create_connect_session

router = APIRouter(prefix="/nango", tags=["Nango"])

@router.post("/connect")
def start_google_drive_connect(user_id: str = "dev-user"):
    session = create_connect_session(user_id)
    return session
