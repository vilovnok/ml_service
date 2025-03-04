from .config import TunedModel
from pydantic import BaseModel, Field
from datetime import datetime

class VerifyCreate(BaseModel):
    user_id: int
    code: int = Field(gt=100000, lt=999999)

class VerifyCreateV2(BaseModel):
    user_id: int
    code: str

class VerifyUserID(BaseModel):
    user_id: int

class VerifyRead(TunedModel):
    id: int
    user_id: int
    code: int = Field(gt=100000, lt=999999)
    created_at: datetime
    is_active: bool

