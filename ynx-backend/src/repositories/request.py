from models.request import Request
from utils.repository import SQLAlchemyRepository

class RequestRepository(SQLAlchemyRepository):
    model = [Request]