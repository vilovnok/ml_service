from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from .config import TunedModel
from typing import List

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str 
    email: EmailStr
    hashed_password: str

class UsersRead(TunedModel):
    id: int
    first_name: str
    last_name: str
    username: str 
    email: EmailStr
    role: str
    balance: int = 100
    avatar_image: str | None
    is_active: bool
    is_verified: bool
    created_at: datetime

class UsersReadAll(BaseModel):
    posts: List[UsersRead]

class GetUsernameCustomer(BaseModel):
    user_id:int 

class SaveEditUser(BaseModel):
    user_id: int
    username:str
    email:EmailStr
    role:str
    active:bool

class AddUser(BaseModel):
    first_name: str
    last_name: str
    username: str 
    email: EmailStr
    is_active: bool
    role: str
    is_verified: bool
    hashed_password: str = Field(min_length=8)