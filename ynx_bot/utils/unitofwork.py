from typing import Type
from abc import ABC, abstractmethod

from ynx_bot.db import AsyncSession, async_session_maker
from ynx_bot.repositories.register import RegisterRepository


class IUnitOfWork(ABC):
    register: Type[RegisterRepository]

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError
    
    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError
    
    @abstractmethod
    async def commit(self):
        raise NotImplementedError
    
    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.register = RegisterRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
