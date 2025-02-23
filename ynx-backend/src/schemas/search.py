from datetime import datetime
from pydantic import (BaseModel, EmailStr, UUID4)
from fastapi import UploadFile, File
from .config import TunedModel
from typing import List


class DATASETS(TunedModel):
    dsid: int
    dsn: str
    date:datetime

class DATASETSAllRead(BaseModel):
    post: List[DATASETS]

class EventRead(TunedModel):
    run_number: int    
    event_number: int    
    type: str    
    version: str
    dsid: int
    fuid_raw: UUID4

class EventAllRead(BaseModel):
    events: List[EventRead]

class ReqEvent(BaseModel):
    run_number: int    
    event_number: int    
    type: str    
    version: str    

class PostRead(TunedModel):
    id: int
    user_id: int
    username: str
    email: EmailStr
    status: str
    sys_task_id: str
    count_req: int
    created_at: datetime     

class Post_to(BaseModel):
    user_id: int
    username: str
    email: EmailStr    
    count_req: int
    status: str
    sys_task_id: str

class PostReadAll(BaseModel):    
    posts: List[PostRead]

class DownloadFile(BaseModel):
    task_id: str