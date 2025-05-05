from datetime import datetime
from db.db import Base
from sqlalchemy import (Column, String, Integer,
                        TIMESTAMP, Boolean,text)
from sqlalchemy.orm import Mapped, mapped_column
from schemas.user import *

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False, primary_key=True, index=True)
    email = Column(String, nullable=False, primary_key=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default='user')
    balance = Column(Integer, nullable=False, default=100)
    avatar_image = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'),onupdate=text('CURRENT_TIMESTAMP'))

    def to_read_model(self) -> UsersRead:
        return UsersRead(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            email=self.email,
            role=self.role,
            balance=self.balance,
            avatar_image=self.avatar_image,
            is_active=self.is_active,
            is_verified=self.is_verified,
            created_at=self.created_at
        )