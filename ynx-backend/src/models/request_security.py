from schemas.request_security import *

from db.db import Base
from sqlalchemy import (Column, TIMESTAMP, Integer, ForeignKey, String)
from sqlalchemy.orm import Mapped, mapped_column


class RequestSecurity(Base):
    __tablename__ = 'request_security'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    status = Column(String, nullable=False, default='pending')
    token = Column(String, nullable=True)
    message = Column(String, nullable=True)
    message_gen = Column(String, nullable=True)
    started_at = Column(TIMESTAMP(timezone=True), nullable=True)
    finished_at = Column(TIMESTAMP(timezone=True), nullable=True)

    def to_read_model(self) -> RequestSecurityRead:
        return RequestSecurityRead(
            user_id=self.user_id,
            status=self.status,
            token=self.token,
            message_gen=self.message_gen,
            message=self.message,
            started_at=self.started_at,
            finished_at=self.finished_at
        )  