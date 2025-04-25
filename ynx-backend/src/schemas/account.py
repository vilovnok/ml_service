from .config import TunedModel
from pydantic import BaseModel, Field


class AccountUserID(BaseModel):
    user_id: int

class AccountRead(TunedModel):
    user_id: int
    balance: int = 100
    gate: str = 'easy'
    

