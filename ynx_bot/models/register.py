from ynx_bot.db import Base
from sqlalchemy import (Column, Integer, ForeignKey, 
                        TIMESTAMP, Boolean, text)
from sqlalchemy.orm import Mapped, mapped_column
from ynx_bot.schemas.register import RegisterRead

class Register(Base):
    __tablename__ = 'register'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, unique=True)
    is_verify = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'),onupdate=text('CURRENT_TIMESTAMP'))

    def to_read_model(self) -> RegisterRead:
        return RegisterRead(
            id=self.id,
            user_id=self.user_id,
            created_at=self.created_at,
            is_verify=self.is_verify,
            is_active=self.is_active,
        )