from ynx_bot.utils.unitofwork import IUnitOfWork, UnitOfWork
from fastapi import HTTPException


class RegisterServices:

    async def get_one(uow: IUnitOfWork, user_id: int):
        async with uow:
            try:
                user = await uow.register.get_one(id=user_id, n_tab=0)
                if not user:
                    return 'User is not registered'
                return user
            except HTTPException as err:
                    await uow.rollback()
                    raise HTTPException(status_code=err.status_code, detail=err)          