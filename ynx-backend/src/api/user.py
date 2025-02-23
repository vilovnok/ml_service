from schemas.user import *
from .dependencies import *
from fastapi import APIRouter
from services.user import UsersService


router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.get('/profiles', status_code=200, response_model=UsersReadAll)
async def get_users_profiles(
    uow: UOWDep,
    user: CurrentUser
):
    profiles = await UsersService().get_all_user(uow, user)
    return profiles

@router.post('/profile', status_code=200, response_model=UsersRead)
async def get_user_profile(
    uow: UOWDep,
    data: GetUsernameCustomer
):
    profiles = await UsersService().get_user_by_user_id(uow, data)
    return profiles

@router.post('/save', status_code=200)
async def save_user_profile(
    uow: UOWDep,
    admin:VerifiedAdmin,
    data: SaveEditUser
):
    res = await UsersService().update_profile(uow, data)
    return res

@router.post('/add', status_code=200)
async def add_user_profile(
    uow: UOWDep,
    admin:VerifiedAdmin,
    data: SaveEditUser
):
    res = await UsersService().add_profile(uow, data)
    return res

@router.post('/remove', status_code=200)
async def remove_user_profile(
    uow: UOWDep,
    admin:VerifiedAdmin,
    data: GetUsernameCustomer
):
    res = await UsersService().remove_profile(uow, data)
    return res

@router.get('/get-profile-by-username/{username}', status_code=200)
async def get_profile(
    user: CurrentUser,
    uow: UOWDep,
    username: str
):
    res = await UsersService().get_user_by_username(uow, username)
    return res

@router.get('/get-profile-by-email/{email}', status_code=200)
async def get_profile(
    user: CurrentUser,
    uow: UOWDep,
    email: EmailStr
):
    res = await UsersService().get_user_by_email(uow, email)
    return res