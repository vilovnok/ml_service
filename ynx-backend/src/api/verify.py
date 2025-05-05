from .dependencies import *
from schemas.verify import *
from fastapi import APIRouter
from services.verify import VerifyService


router = APIRouter(
    prefix='/verify',
    tags=['Verify']
)

@router.get('/get-code/{user_id}')
async def get_verify_code(
    user_id: int,
    uow: UOWDep
):
    res = await VerifyService().get_verify_code(uow, user_id)
    return res

@router.post('/send-code')
async def send_code(
    data: VerifyCreateV2,
    uow: UOWDep
):
    res = await VerifyService().send_verify_code(uow, data)
    return res

@router.get('/verify-user/{user_id}',status_code=200)
async def get_verify_user_data(
    user_id: int,
    uow: UOWDep
):
    res = await VerifyService().get_verify_user_data(uow, user_id)
    return res