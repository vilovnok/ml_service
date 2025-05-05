from utils.unitofwork import IUnitOfWork
from fastapi import HTTPException
from schemas.user import *
from models.user import Users
from datetime import datetime, timezone, timedelta
from auth.auth import bcrypt_context

class UsersService:
    async def get_all_user(self, uow: IUnitOfWork, user: UsersRead):
        async with uow:
            users = await uow.user.get_all(n_tab=0)
            users_profile = UsersReadAll(**user.model_dump(), posts=users)
            return users_profile     

    async def get_user_by_user_id(self, uow: IUnitOfWork, data: GetUsernameCustomer):
        async with uow:
            user = await uow.user.get_one(id=data.user_id,n_tab=0)
            if not user:
                await uow.rollback()
                raise HTTPException(status_code=404, detail='The user was not found!')
            posts = await uow.user.get_all(username=user.username,n_tab=0)
            user_profile = UsersRead(**user.model_dump(), posts=posts)
            return user_profile   
        
    async def get_user_by_username(self, uow: IUnitOfWork, username: str):
        async with uow:
            user = await uow.user.get_one(username=username,n_tab=0)
            if not user:
                await uow.rollback()
                raise HTTPException(status_code=404, detail='The user was not found!')
            posts = await uow.user.get_all(username=user.username,n_tab=0)
            user_profile = UsersRead(**user.model_dump(), posts=posts)
            return user_profile   
        
    async def get_user_by_email(self, uow: IUnitOfWork, email: EmailStr):
        async with uow:
            user = await uow.user.get_one(email=email,n_tab=0)
            if not user:
                await uow.rollback()
                raise HTTPException(status_code=404, detail='The user was not found!')
            posts = await uow.user.get_all(username=user.username,n_tab=0)
            user_profile = UsersRead(**user.model_dump(), posts=posts)
            return user_profile       

    async def update_profile(self, uow: IUnitOfWork, data: SaveEditUser):
        async with uow:
            try:                
                user = await uow.user.get_one(id=data.user_id, n_tab=0)
                current_time=datetime.now().replace(microsecond=0)
                time_with_timezone=current_time.replace(tzinfo=timezone(timedelta(hours=3)))

                if not user:
                    await uow.rollback()
                    raise HTTPException(status_code=404, detail='User not found')                
                await uow.user.update(where=[Users.id==data.user_id], n_tab=0, values={'username': data.username, 
                                                                        'email': data.email, 
                                                                        'role': data.role,
                                                                        'is_active':data.active,
                                                                        'updated_at':time_with_timezone})
                await uow.commit()
                return {
                    'status': 'success',
                    'message': f'Пользователь успешно обнавлен'
                }
            except HTTPException as err:
                raise HTTPException(status_code=err.status_code)
            except:
                await uow.rollback()
                raise HTTPException(status_code=400)  


    async def add_profile(self, uow: IUnitOfWork, data: SaveEditUser):
        first_name='admin'
        last_name='admin'
        password='admin'
        async with uow:
                email_checker = await uow.user.get_one(email=data.email,n_tab=0)
                username_checker = await uow.user.get_one(username=data.username,n_tab=0)                
               
                if email_checker:
                    await uow.rollback()
                    raise HTTPException(status_code=400, detail='A user with this email already exists')
                if username_checker:
                    await uow.rollback()
                    raise HTTPException(status_code=400, detail='A user with this username already exists')                
            
                user_model = AddUser(
                    first_name=first_name,
                    last_name=last_name,
                    username=data.username,
                    email=data.email,
                    role=data.role,
                    is_verified=True,
                    is_active=data.active,
                    hashed_password=bcrypt_context.hash(password)
                )
                user_id = await uow.user.add_one(user_model.model_dump(), n_tab=0)         
                if not user_id:
                    await uow.rollback()
                    raise HTTPException(status_code=400)                
                await uow.commit()
                res= {'status': 'success',
                    'message': f'The user with user_id={user_id} has been successfull added'}
                return res             
            
    async def remove_profile(self, uow: IUnitOfWork, data: GetUsernameCustomer):
        async with uow:
            user = await uow.user.get_one(id=data.user_id,n_tab=0)
            if not user:
                await uow.rollback()
                raise HTTPException(status_code=400, detail='User was previously removed')
            await uow.verify.delete(user_id=user.id,n_tab=0)
            await uow.request.delete(user_id=user.id, n_tab=0) 
            await uow.request_security.delete(user_id=user.id, n_tab=0) 
            await uow.user.delete(id=user.id,n_tab=0)
            await uow.commit()
            return {
                'status': 'success',
                'message': 'User successfully deleted'
            }    