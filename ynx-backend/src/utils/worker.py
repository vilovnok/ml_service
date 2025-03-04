import smtplib
from config import *
from utils.mail import *
from celery import Celery
from models.search import *


celery = Celery(
    __name__, 
    # broker=f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_DEFAULT_HOST}:{RABBITMQ_DEFAULT_PORT}",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}",
)

@celery.task
def send_email_code(username:str, email:str, code:int):
    email_template = get_email_template_code(username=username, email=email, code=code)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(EMAIL_SEND, EMAIL_PASS)
        server.send_message(email_template)


# @celery.task
# def send_email_file(email: str,
#                     filename:str,
#                     percent:str,
#                     dataset:str):
#     email_template = get_email_template_file(
#         email=email,filename=filename,
#         percent=percent,dataset=dataset)
#     if not email_template:
#         return None
#     try:
#         server=smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
#         server.login(EMAIL_SEND, EMAIL_PASS)
#         server.sendmail(EMAIL_SEND,email,email_template) 
#         server.quit()       
#     except Exception:
#         return None              


# @celery.task
# def send_email_zipfiles(email: str, filename:str) -> None:    
#     email_template = get_email_template_files_debug(email=email,filename=filename)
#     if not email_template:
#         return None
#     try:
#         server=smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
#         server.login(EMAIL_SEND, EMAIL_PASS)
#         server.sendmail(EMAIL_SEND, email, email_template) 
#         server.quit()                   
#     except Exception:
#         return None   


# @celery.task
# def send_email_files_by_date(email:str, user_id:int, start_date:datetime, end_date:datetime):
#     try:
#         conn = conn_to_db() 
#         cursor = conn.cursor() 
#         filenames=[]
#         query = """SELECT filename_prfx_raw, filename_prfx_prep
#                    FROM pipeline WHERE duration_time>=%s AND duration_time<=%s AND user_id=%s"""
#         cursor.execute(query, (start_date, end_date, user_id))
#         filenames_prefix_raw_prep = cursor.fetchall()
#         for filename_prefix_raw_prep in filenames_prefix_raw_prep:
#             filenames.append({'filename_raw':filename_prefix_raw_prep[0],'filename_prep':filename_prefix_raw_prep[1]})   
#         if len(filenames)<=0:
#             return None        
#         send_email_zipfiles.delay(email,filenames,type='from_zf')        
#     except Exception:
#         return None 

# @celery.task
# def preprocessingDataTask(args):   
#     file_manager=FileManager()
#     conn=conn_to_db()
#     cursor = conn.cursor() 
#     fuids_raw = []
#     email=args['email']
#     user_id=args['user_id']
#     sys_task_id=args['sys_task_id']    
#     filename_raw=args['filename_raw']
#     filename_prep=args['filename_prep']
#     finded_patterns=file_manager.preprocessing_file(filename=filename_raw)    
#     count=len(finded_patterns['run_numbers'])
#     try:
#         for i in range(count): 
#             run_number = finded_patterns['run_numbers'][i]
#             event_number = finded_patterns['event_numbers'][i]
#             version = finded_patterns['versions'][i]
#             type = finded_patterns['types'][i]

#             query = f"""
#                     SELECT fuid_raw FROM events WHERE 
#                     run_number = %s AND event_number = %s AND
#                     version = %s AND type = %s;
#                     """
#             cursor.execute(query, (run_number, event_number, version, type))
#             fuid_raw=cursor.fetchone()
#             fuids_raw.append(fuid_raw)
#         try:
#             query = f"""
#                     UPDATE pipeline SET status = 'success'
#                     WHERE sys_task_id = %s AND user_id = %s;
#                     """     
#             cursor.execute(query,(sys_task_id, user_id))
#             query = f"""
#                     UPDATE post SET status = 'success'
#                     WHERE sys_task_id = %s AND user_id = %s;
#                     """     
#             cursor.execute(query,(sys_task_id, user_id))
#             conn.commit()    
#         except Exception as err:
#             print(f'Error: {err}')    

#         file_manager.generate_file_from_fuid(fuids=fuids_raw,filename=filename_prep)
#         file_manager.save_file_to_zf(filename=filename_prep,type='prep')
#         filenames=[{'filename_raw':filename_raw,'filename_prep':filename_prep}]
#         send_email_zipfiles.delay(email=email,filenames=filenames,type='from_dir')
#     except Exception:
#         query = f"""
#                 UPDATE pipeline SET status = 'faile'
#                 WHERE sys_task_id = %s AND user_id = %s;
#                 """     
#         cursor.execute(query,(sys_task_id, user_id))
#         query = f"""
#                 UPDATE post SET status = 'faile'
#                 WHERE sys_task_id = %s AND user_id = %s;
#                 """     
#         cursor.execute(query,(sys_task_id, user_id))
#         conn.commit()       
#     finally:
#        if conn:
#            cursor.close()        

# @celery.task
# def extract_file_data(kwargs:dict):  
#     fileManager = FileManagerDebug()
#     conn=conn_to_db()
#     cursor = conn.cursor()
#     fuids_raw = []
#     email=kwargs['email']
#     user_id=kwargs['user_id']
#     file_name=kwargs['file_name']
#     sys_task_id=kwargs['sys_task_id']
    
#     file_data=fileManager.get_file(bucket_name='evin-raw', file_name=file_name)
#     finded_patterns = fileManager.preprocessing_file(file_data=file_data)
#     count=len(finded_patterns['run_numbers'])
#     try:
#         for i in range(count): 
#             run_number = finded_patterns['run_numbers'][i]
#             event_number = finded_patterns['event_numbers'][i]
#             version = finded_patterns['versions'][i]
#             type = finded_patterns['types'][i]

#             query = f"""
#                     SELECT fuid_raw FROM events WHERE 
#                     run_number = %s AND event_number = %s AND
#                     version = %s AND type = %s;
#                     """
#             cursor.execute(query, (run_number, event_number, version, type))
#             fuid_raw=cursor.fetchone()
#             fuids_raw.append(fuid_raw)
#         try:
#             query = f"""
#                     UPDATE pipeline SET status = 'success'
#                     WHERE sys_task_id = %s AND user_id = %s;
#                     """     
#             cursor.execute(query,(sys_task_id, user_id))
#             query = f"""
#                     UPDATE post SET status = 'success'
#                     WHERE sys_task_id = %s AND user_id = %s;
#                     """     
#             cursor.execute(query,(sys_task_id, user_id))
#             conn.commit()    
#         except Exception as err:
#             raise ValueError(f'Error: {err}')

#         path = fileManager.generate_file_from_fuid(fuids=fuids_raw,filename=file_name)
#         fileManager.upload_obj_path(file_name=file_name, file_path=path, bucket_name='evin-processed')        
#         send_email_zipfiles.delay(email=email,filename=file_name)
#         os.remove(path)
#     except:
#         query = f"""
#                 UPDATE pipeline SET status = 'faile'
#                 WHERE sys_task_id = %s AND user_id = %s;
#                 """     
#         cursor.execute(query,(sys_task_id, user_id))
#         query = f"""
#                 UPDATE post SET status = 'faile'
#                 WHERE sys_task_id = %s AND user_id = %s;
#                 """     
#         cursor.execute(query,(sys_task_id, user_id))
#         conn.commit()       
#     finally:
#        if conn:
#            cursor.close()