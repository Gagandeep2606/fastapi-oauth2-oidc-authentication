from datetime import datetime
from pydantic import BaseModel,Field


class refresh_token(BaseModel):
    user_id:str
    token:str
    expires_at:datetime
    revoke: bool=False
    created_at:datetime=Field(default_factory=datetime.utcnow)