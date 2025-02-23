from fastapi import Depends
from typing import Annotated
from ynx_bot.utils.unitofwork import IUnitOfWork, UnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]