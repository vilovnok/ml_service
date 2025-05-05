from auth.auth import *
from fastapi import Depends
from typing import Annotated
from schemas.user import UsersRead
from utils.unitofwork import IUnitOfWork, UnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
CurrentUser = Annotated[UsersRead, Depends(get_current_user)]
VerifiedUser = Annotated[UsersRead, Depends(get_verified_user)]
VerifiedAdmin = Annotated[UsersRead, Depends(get_verify_admin)]