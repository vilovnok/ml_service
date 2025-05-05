from fastapi import APIRouter
from .dependencies import UOWDep
from services.auth import AuthService
from schemas.auth import AuthRegister, AuthLogin, AuthForgetPass
from schemas.token import TokenCreate, TokenRefresh

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post('/register', status_code=201)
async def register(
    data: AuthRegister,
    uow: UOWDep
):
    res = await AuthService().register(uow, data)
    return res

@router.post('/login', status_code=200, response_model=TokenCreate)
async def login(
    data: AuthLogin,
    uow: UOWDep
):
    access_token, refresh_token = await AuthService().login(uow, data)
    return TokenCreate(
        access_token=access_token, 
        refresh_token=refresh_token, 
        token_type='bearer')

@router.post('/reset-password', status_code=200)
async def reset_password(
    data: AuthForgetPass,
    uow: UOWDep
):
    res = await AuthService().reset_password(uow=uow, data=data)  
    return res

@router.post('/refresh-token', status_code=200, response_model=TokenCreate)
async def refresh_token(
    data: TokenRefresh,
    uow: UOWDep
):
    access_token, refresh_token = await AuthService().refresh_token(uow, data)
    return TokenCreate(
        access_token=access_token, 
        refresh_token=refresh_token, 
        token_type='Bearer')
