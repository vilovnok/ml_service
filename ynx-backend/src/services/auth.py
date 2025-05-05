from utils.unitofwork import IUnitOfWork
from schemas.auth import AuthRegister, AuthLogin, AuthForgetPass
from schemas.user import UserCreate
from schemas.token import TokenRefresh, TokenData
from auth.auth import bcrypt_context, create_access_token, decode_token
from fastapi.exceptions import HTTPException
from models.user import Users
from datetime import timedelta
from config import SECRET, REFRESH_SECRET, ALGORITHM



class AuthService:
    async def register(self, uow: IUnitOfWork, data: AuthRegister):
        user_model = UserCreate(
            first_name=data.first_name,
            last_name=data.last_name,
            username=data.username,
            email=data.email,
            hashed_password=bcrypt_context.hash(data.password)
        )

        async with uow:
            email_checker = await uow.user.get_one(email=data.email, n_tab=0)
            username_checker = await uow.user.get_one(username=data.username, n_tab=0)
            is_verified_email_checker = await uow.user.get_one(email=data.email, is_verified=True, n_tab=0)            
            is_verified_username_checker = await uow.user.get_one(username=data.username, is_verified=True, n_tab=0)
            
            if email_checker:
                if is_verified_email_checker:            
                    await uow.rollback()
                    raise HTTPException(status_code=400, detail='Пользователь с таким email уже существует!')
                
                await uow.user.update(where=[Users.id==email_checker.id], n_tab=0,
                                                values={
                                                    'first_name':data.first_name,
                                                    'last_name':data.last_name,
                                                    'username': data.username, 
                                                    'email': data.email, 
                                                    'hashed_password':bcrypt_context.hash(data.password)})
                await uow.commit()
                res = {'status': 'success',
                        'user_id': email_checker.id, 
                        'message':"Введите code из вашей почты: ******"}
                return res
            if username_checker:
                if is_verified_username_checker:
                    await uow.rollback()
                    raise HTTPException(status_code=400, detail='Пользователь с таким username уже существует!')
                
                await uow.user.update(where=[Users.id==username_checker.id],n_tab=0,
                                                values={
                                                    'first_name':data.first_name,
                                                    'last_name':data.last_name,
                                                    'username': data.username, 
                                                    'email': data.email, 
                                                    'hashed_password':bcrypt_context.hash(data.password)})
                await uow.commit()
                res = {'status': 'success',
                        'user_id': username_checker.id, 
                        'message':"Введите code из вашей почты: ******"}
                return res                                        
            
            try:
                user_id = await uow.user.add_one(user_model.model_dump(), n_tab=0)
                await uow.commit()
            except Exception:
                await uow.rollback()
                raise HTTPException(status_code=400)

            user_id = 1 if user_id is None else user_id.id

            res = {'status': 'success',
                   'user_id': user_id, 
                   'message':"Введите code из вашей почты: ******"}
            return res

    async def login(self, uow: IUnitOfWork, data: AuthLogin):
        async with uow:
            user: Users = await uow.user.get_one(email= data.email, full_model=True,n_tab=0)            
            if not user:            
                await uow.rollback()
                raise HTTPException(status_code=400, detail='Invalid password or email')
            if not bcrypt_context.verify(data.password, user.hashed_password):
                await uow.rollback()
                raise HTTPException(status_code=400, detail='Invalid password or email')
            access_token = create_access_token(username=user.username, 
                                               user_id=user.id,
                                               first_name=user.first_name,
                                               last_name=user.last_name,
                                               role=user.role,
                                               verify=user.is_verified,
                                               active=user.is_active,
                                               balance=user.balance,
                                               ava_img=user.avatar_image, 
                                               secret=SECRET, 
                                               expires_delta=timedelta(hours=3))
            refresh_token = create_access_token(username=user.username, 
                                                user_id=user.id,
                                                first_name=user.first_name,
                                                last_name=user.last_name,
                                                role=user.role, 
                                                verify=user.is_verified,
                                                active=user.is_active,
                                                balance=user.balance,
                                                ava_img=user.avatar_image, 
                                                secret=REFRESH_SECRET, 
                                                expires_delta=timedelta(days=3))
            return access_token, refresh_token
        
    async def reset_password(self, uow: IUnitOfWork, data: AuthForgetPass):
        async with uow:
            user = await uow.user.get_one(email=data.email, n_tab=0)
            if not user:            
                await uow.rollback()
                raise HTTPException(status_code=400, detail='User with email is not exists.')
        
            await uow.user.update(where=[Users.email==data.email], n_tab=0,
                                            values={'hashed_password' : bcrypt_context.hash(data.password)})
            await uow.commit()
            res = {'status': 'success', 'message':"Your password has been reset."}
            return res

    async def refresh_token(self, uow: IUnitOfWork, data: TokenRefresh):
        if data.token_type.lower() != 'bearer':
            await uow.rollback()
            raise HTTPException(status_code=400, detail='Invalid token type')
        async with uow:
            try:
                token_data: TokenData = decode_token(data.refresh_token, REFRESH_SECRET, ALGORITHM) 
                user = await uow.user.get_one(id=token_data.id, username=token_data.sub,n_tab=0)
                access_token = create_access_token(username=user.username, 
                                                   user_id=user.id,
                                                   first_name=user.first_name,
                                                   last_name=user.last_name,
                                                   role=user.role,
                                                   verify=user.is_verified,
                                                   active=user.is_active,
                                                   balance=user.balance,
                                                   ava_img=user.avatar_image, 
                                                   secret=SECRET, 
                                                   expires_delta=timedelta(hours=3))
                refresh_token = create_access_token(username=user.username, 
                                                    user_id=user.id,
                                                    first_name=user.first_name,
                                                    last_name=user.last_name,
                                                    role=user.role, 
                                                    verify=user.is_verified,
                                                    active=user.is_active,
                                                    balance=user.balance,
                                                    ava_img=user.avatar_image, 
                                                    secret=REFRESH_SECRET, 
                                                    expires_delta=timedelta(days=3))
                return access_token, refresh_token
            except Exception:
                await uow.rollback()
                raise HTTPException(status_code=400, detail='Invalid token')