from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .config import TunedModel



class RequestSecurityRead(TunedModel):
    user_id: int
    status: str = Field(default='pending') 
    token: str
    message: str
    message_gen: str = Field(default='')
    started_at: datetime
    finished_at: datetime = Field(default=None) 

class RequestSecurityRead(BaseModel):
    posts: List[RequestSecurityRead]

class RequestSecurityCreate(BaseModel):
    user_id: int
    token: str
    message: str
    started_at: datetime

class RequestEntityV1(BaseModel):
    message: str

class RequestEntityV2(BaseModel):
    user_id: int