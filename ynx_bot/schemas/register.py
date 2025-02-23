from .config import TunedModel
from datetime import datetime


class RegisterRead(TunedModel):
    id: int
    username: str
    created_at: datetime
    is_verify: bool
    is_active: bool