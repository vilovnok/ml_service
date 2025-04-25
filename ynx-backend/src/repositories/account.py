from models.account import Account
from utils.repository import SQLAlchemyRepository

class AccountRepository(SQLAlchemyRepository):
    model = [Account]