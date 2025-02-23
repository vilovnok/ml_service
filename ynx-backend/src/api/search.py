from services.search import *
from fastapi import APIRouter
from .dependencies import CurrentUser, UOWDep

router = APIRouter(
    prefix='/search',
    tags=['Search']
)

# @router.post('/get-fuid-raw', status_code=200)
# async def get_fuid_raw(
#     user: CurrentUser,
#     uow: UOWDep,
#     data: ReqEvent
# ):
#     res = await SearchService().get_fuid_raw(uow, data, user)
#     return res

# @router.post('/upload-file', status_code=200)
# async def upload_file(
#     user: CurrentUser,
#     uow: UOWDep,
#     file: UploadFile,    
# ):
#     # res = await SearchService().upload_file(uow, file, user)
#     res = await SearchService().upload_file_debug(uow, file, user)
#     return res