from models.verify import Verify
from utils.repository import SQLAlchemyRepository

class VerifyRepository(SQLAlchemyRepository):
    model = [Verify]
    