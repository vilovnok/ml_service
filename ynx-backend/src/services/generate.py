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
                if user.balance <= 9:
                    raise HTTPException(status_code=403, detail=f"На вашем балансе {user.balance} YNX. Для взаимодействия с моделью требуется не менее 10 YNX 🧑‍🔧")

                await uow.request.add_one(request_model.model_dump(), n_tab=0)
                await uow.commit()
                generate_text.delay(user_id=user_id, message=message, token=token)

                return {"token": token}

    async def get_chat(self, uow: IUnitOfWork, user: UsersRead):
        async with uow:
            try:
                messages = await uow.request.get_all(user_id=user.id, n_tab=0)
                messages = RequestAllRead(**user.model_dump(), posts=messages)
                if messages:
                    return {                                        
                        "messages": messages
                    }   
                print('4'*100)         
            except Exception as err:
                print(err)
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
            
    async def get_balance(self, uow: IUnitOfWork, user: UsersRead):
        async with uow:            
            return {'balance': user.balance}


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
            if message is None:
                raise HTTPException(status_code=404, detail="Message not found")
            
            status = message.status 
            balance = user.balance
            message_gen = message.message_gen

            if status == 'completed':
                return {'status': status, 'message_gen': message_gen, 'balance': balance}
