from datetime import datetime
from db.db import Base
from sqlalchemy import (Column, TIMESTAMP, BIGINT,UUID,
                        Integer, ForeignKey, String,text)
from sqlalchemy.orm import Mapped, mapped_column
from schemas.account import *


class Account(Base):
    __tablename__ = 'account'
    __table_args__ = {'extend_existing': True}

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    balance = Column(Integer, nullable=False, default=100)
    gate = Column(String, nullable=False, default='easy')

    def to_read_model(self) -> AccountRead:
        return AccountRead(
            user_id=self.user_id,
            balance=self.balance,
            gate=self.gate
        )  