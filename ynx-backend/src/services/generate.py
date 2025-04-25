import time
import uuid

from fastapi import HTTPException

from models.request import *
from models.request_security import *
from schemas.user import *
from utils.worker import generate_text, topUpBalance
from utils.unitofwork import IUnitOfWork

from datetime import datetime
from zoneinfo import ZoneInfo




class GenerateService:
    async def generate(self, uow: IUnitOfWork, user: UsersRead, data: RequestEntityV1):
            async with uow:
                token = str(uuid.uuid4())
                user_id=user.id
                message=data.message
                started_at = datetime.now(ZoneInfo("Europe/Moscow"))
                
                request_model = RequestCreate(
                    user_id=user_id,
                    token=token,
                    message=message,
                    started_at=started_at,
                )
                balance = await uow.account.get_one(user_id=user.id, n_tab=0)
                if balance.balance <= 0:
                    raise HTTPException(status_code=403, detail=f"На вашем балансе {balance.balance} YNX. Для взаимодействия с моделью требуется не менее 10 YNX 🧑‍🔧")
                if balance.balance <= 9:
                    raise HTTPException(status_code=403, detail=f"На вашем балансе {balance.balance} YNX. Для взаимодействия с моделью требуется не менее 10 YNX 🧑‍🔧")

                await uow.request.add_one(request_model.model_dump(), n_tab=0)
                await uow.commit()
                generate_text.delay(user_id=user_id, message=message, token=token)

                return {"token": token}

    async def get_chat(self, uow: IUnitOfWork, data: UsersRead):
        async with uow:
            user_id = data.id
            try:
                messages = await uow.request.get_all(user_id=user_id, n_tab=0)
                messages = RequestAllRead(**data.model_dump(), posts=messages)
                if messages:
                    return {                                        
                        "messages": messages
                    }            
            except Exception as err:
                raise HTTPException(status_code=400, detail=f"{err}")      
            

    async def get_message(self, uow: IUnitOfWork, token: str):
        async with uow:
            message = await uow.request.get_one(token=token, n_tab=0)
            
            if message is None:
                raise HTTPException(status_code=404, detail="Message not found")
            
            status = message.status 
            if status!='completed':
                return {'status': status, 'message_gen': None}
            else:
                return {'status': status, 'message_gen': message.message_gen}
            

    async def topUpBalance(self, uow: IUnitOfWork, user: UsersRead, data: RequestEntityV1):
            async with uow:
                token = str(uuid.uuid4())
                user_id=user.id
                message=data.message
                started_at = datetime.now(ZoneInfo("Europe/Moscow"))
                
                request_model = RequestSecurityCreate(
                    user_id=user_id,
                    token=token,
                    message=message,
                    started_at=started_at,
                )
                await uow.request_security.add_one(request_model.model_dump(), n_tab=0)
                await uow.commit()
                topUpBalance.delay(user_id=user_id, message=message, token=token)

                return {"token": token}


    async def check_balance(self, uow: IUnitOfWork, user: UsersRead, token: str):
        async with uow:
            message = await uow.request_security.get_one(token=token, n_tab=0)
            account = await uow.account.get_one(user_id=user.id, n_tab=0)

            if message is None:
                raise HTTPException(status_code=404, detail="Account not found")
                    
            return {'status': message.status, 'message_gen': message.message_gen, 'balance': account.balance}
        
