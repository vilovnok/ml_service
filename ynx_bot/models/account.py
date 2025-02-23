from sqlalchemy import Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from ynx_bot.db import Base
from schemas.account import AccountRead

class Account(Base):
    __tablename__ = 'account'
    __table_args__ = {'extend_existing': True}

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id', ondelete="CASCADE"), 
        primary_key=True, index=True
    )
    balance: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), default=500)

    def to_read_model(self) -> AccountRead:
        return AccountRead(
            user_id=self.user_id,
            balance=self.balance
        )