from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    content: str
    timestamp: datetime = datetime.utcnow()
    role: str
