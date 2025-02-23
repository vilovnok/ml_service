from .config import TunedModel

class AccountRead(TunedModel):
    user_id: int
    balance: int