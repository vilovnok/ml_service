from fastapi import APIRouter
from services.generate import GenerateService

from .dependencies import *
from models.request import RequestEntityV1


router = APIRouter(
    prefix='/generate',
    tags=['Generate']
)

@router.post('/generate_text', status_code=200)
async def generate_text(
    data: RequestEntityV1,
    user: CurrentUser,
    uow: UOWDep,
):
    res = await GenerateService().generate(uow, user, data)
    return res

@router.get('/get_chat', status_code=200)
async def get_chat(
    user: CurrentUser,
    uow: UOWDep,
):
    res = await GenerateService().get_chat(uow, user)
    return res

@router.get('/get_balance', status_code=200)
async def get_balance(
    user: CurrentUser,
    uow: UOWDep,
):
    res = await GenerateService().get_balance(uow, user)
    return res

@router.get('/get_message/{token}', status_code=200)
async def get_message(
    token: str,
    uow: UOWDep,
):
    res = await GenerateService().get_message(uow, token)
    return res

@router.post('/top-up-balance', status_code=200)
async def security_gen(
    data: RequestEntityV1,
    user: CurrentUser,
    uow: UOWDep,
):
    res = await GenerateService().topUpBalance(uow, user, data)
    return res

@router.get('/check-balance/{token}', status_code=200)
async def check_balance(    
    token: str,
    user: CurrentUser,
    uow: UOWDep,
):
    res = await GenerateService().check_balance(uow, user, token)
    return res