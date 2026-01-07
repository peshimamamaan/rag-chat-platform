from pydantic import BaseModel

class DriveImportRequest(BaseModel):
    file_id: str
    file_name: str
    connection_id: str