from models.request_security import RequestSecurity
from utils.repository import SQLAlchemyRepository

class RequestSecurityRepository(SQLAlchemyRepository):
    model = [RequestSecurity]