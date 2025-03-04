
from auth.auth import create_access_token
from config import REFRESH_SECRET, SECRET
from utils.unitofwork import IUnitOfWork
from random import randint
from models.verify import Verify
from models.user import Users
from schemas.verify import *
from schemas.user import *
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from datetime import datetime, timedelta
import time

from utils.worker import send_email_code


class VerifyService:
    async def send_verify_code(self, uow: IUnitOfWork, data: VerifyCreateV2):
        try:
            async with uow:
                verify = await uow.verify.get_one(user_id=data.user_id, is_active=True,n_tab=0)
            
                if str(verify.code) != data.code:
                    await uow.rollback()
                    raise HTTPException(status_code=400, detail='Incorrect code')
                

                limit_time = datetime.utcnow()
                created_time = verify.created_at + timedelta(minutes=100)                
                
                if created_time.timestamp() < limit_time.timestamp():
                    await uow.rollback()
                    raise HTTPException(status_code=400, detail='Incorrect code')
                
                await uow.user.update(where=[Users.id == verify.user_id], n_tab=0,values={'is_verified': True})
                await uow.verify.update([Verify.user_id == verify.user_id, Verify.is_active == True], {'is_active': False}, n_tab=0)
                await uow.commit()

                res = {"status": 'SUCCESS', "message":'Enter your details'}
                return res
        except NoResultFound:     
            raise HTTPException(status_code=404, detail='Code not found')
        
    async def get_verify_code(self, uow: IUnitOfWork, user_id: str):
        try:
            user_id = int(user_id)            
            async with uow:
                
                
                user = await uow.user.get_one(id=user_id,n_tab=0)
                
                

                if user.is_verified:
                    await uow.rollback()
                    raise HTTPException(status_code=403, message='You have already been verified')
                
                check_verify = await uow.verify.get_one(user_id=user_id,n_tab=0)            
                
                if check_verify:
                    await uow.verify.update([Verify.user_id == user_id, Verify.is_active == True], {'is_active': False},n_tab=0)
                code = randint(100000, 999999)
                model = VerifyCreate(user_id=user_id, code=code)
                user_id = await uow.verify.add_one(model.model_dump(), n_tab=0)
                await uow.commit()
                
                send_email_code.delay(user.username, user.email, code)
                
                
                return {'status':"success",'message':"Enter the verification code","code": code}
        except Exception as error:
            raise HTTPException(status_code=500, detail=error)


    async def get_verify_role_active(self, uow: IUnitOfWork, data: VerifyUserID):
        try:
            async with uow:
                user = await uow.user.get_one(id=data.user_id,n_tab=0)
                if not user:
                    await uow.rollback()
                    raise HTTPException(status_code=404, detail='User not found')
                posts = await uow.user.get_all(username=user.username,n_tab=0)
                user_profile = UsersRead(**user.model_dump(), posts=posts)
                res = {'status':"success", "role": user_profile.role, 'active':user_profile.is_active}
                return res
        except Exception as error:
            raise HTTPException(status_code=500, detail=error)
        


    async def get_verify_user_data(self, uow: IUnitOfWork, user_id: int):
            async with uow:
                user = await uow.user.get_one(id=user_id,n_tab=0)
                if not user:
                    await uow.rollback()
                    raise HTTPException(status_code=404, detail='User not found')
                posts = await uow.user.get_all(username=user.username,n_tab=0)
                user_profile = UsersRead(**user.model_dump(), posts=posts)
                res = {'status':"success", "role": user_profile.role, 'active':user_profile.is_active}
                return res

