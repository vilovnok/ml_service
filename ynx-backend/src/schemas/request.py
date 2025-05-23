from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .config import TunedModel



class RequestRead(TunedModel):
    user_id: int
    status: str = Field(default='pending') 
    token: str
    message: str
    message_gen: str = Field(default='')
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

class RequestAllRead(BaseModel):
    posts: List[RequestRead]

class RequestCreate(BaseModel):
    user_id: int
    token: str
    message: str
    started_at: datetime

class RequestEntityV1(BaseModel):
    message: str

class RequestEntityV2(BaseModel):
    user_id: int