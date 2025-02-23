from ynx_bot.models.register import Register
from ynx_bot.utils.repository import SQLAlchemyRepository

class RegisterRepository(SQLAlchemyRepository):
    model = [Register]