# from utils.fm import FileManager
# from utils.fileManager import FileManager as FileManagerDebug
# from utils.worker import (preprocessingDataTask, send_email_file, extract_file_data)
from utils.unitofwork import IUnitOfWork
from fastapi import HTTPException
from models.search import *
from models.user import *
import uuid


class SearchService:
    pass
    # async def upload_file_debug(self, uow: IUnitOfWork, file:UploadFile, user:UserRead):
    #     async with uow:                  

    #         file_checker = await uow.pipe.get_one(filename=file.filename, n_tab=0)
            
    #         if file_checker:
    #             await uow.rollback()
    #             raise HTTPException(status_code=404, detail='Such a file already exists.')
            
    #         sys_task_id=str(uuid.uuid4())   
    #         file_manager=FileManagerDebug()
    #         file_name = file_manager.generate_filename_with_datetime(file.filename, user.id)

    #         file_manager.upload_obj(file_name=file_name, bucket_name='evin-raw', file_obj=file)
            
    #         data={'file_name':file_name,'user_id':user.id,'email':user.email,'sys_task_id':sys_task_id}
    #         task_id = extract_file_data.delay(data)
            
    #         pipe_model = Pipe_to(
    #             user_id=user.id,
    #             filename=file.filename,
    #             filename_prfx=file_name,                
    #             status='pending',
    #             task_id=str(task_id),
    #             sys_task_id=sys_task_id)        
                
    #         post_model = Post_to(
    #             user_id=user.id,
    #             username=user.username,
    #             email=user.email,
    #             status='pending',
    #             sys_task_id=sys_task_id,
    #             count_req=123)        
            
    #         await uow.search.add_one(pipe_model.model_dump(), n_tab=2)
    #         await uow.search.add_one(post_model.model_dump(), n_tab=1)
    #         await uow.commit()
    #         raise HTTPException(status_code=201)