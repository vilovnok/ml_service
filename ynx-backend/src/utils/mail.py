from config import *
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart



def get_email_template_code(username: str, email: str, code: int):
    email_m = EmailMessage()
    email_m['Subject'] = 'Verification code'
    email_m['From'] = f'YanixTrade {EMAIL_SEND}'
    email_m['To'] = email
    code_to_list = list(str(code))
    email_m.set_content(
        '<div>'
            f'<h1 style="text-align: center;">Hello, {username}! Please use verification code to complete the registration:</h1>'
            '<div style="padding: 20px; display: flex; justify-content: center; align-items: center; gap: 5px;">'
                '<div style="padding: 0px 15px; border: 2px solid; border-color: red; border-radius: 5px;">'
                    f'<h1>{code_to_list[0]}</h1>'
                '</div>'
                '<div style="padding: 0px 15px; border: 2px solid; border-color: red; border-radius: 5px;">'
                    f'<h1>{code_to_list[1]}</h1>'
                '</div>'
                '<div style="padding: 0px 15px; border: 2px solid; border-color: red; border-radius: 5px;">'
                    f'<h1>{code_to_list[2]}</h1>'
                '</div>'
                '<div style="padding: 0px 15px; border: 2px solid; border-color: red; border-radius: 5px;">'
                    f'<h1>{code_to_list[3]}</h1>'
                '</div>'
                '<div style="padding: 0px 15px; border: 2px solid; border-color: red; border-radius: 5px;">'
                    f'<h1>{code_to_list[4]}</h1>'
                '</div>'
                '<div style="padding: 0px 15px; border: 2px solid; border-color: red; border-radius: 5px;">'
                    f'<h1>{code_to_list[5]}</h1>'
                '</div>'
            '</div>'
        '</div>',
        subtype='html'
    )
    return email_m


# def get_email_template_file(email:str,
#                             filename:str,
#                             percent:str,
#                             dataset:str):
#     text = f"The zip file contains {percent}% of the events from {dataset}."
#     try:
#         msg = MIMEMultipart()
#         msg["Subject"] = 'The zip file contains events'       
#         msg["From"] = f'SPD {EMAIL_SEND}' 
#         msg["To"] = email
        
#         file_manager = FileManagerDebug()
#         zip_filename='arch.zip'  
#         file_content = file_manager.get_file(bucket_name='evin-temp',
#                                              file_name=filename)
        
#         zip_path = file_manager.create_zip_file_by_content(file_content=file_content, 
#                                      zip_filename=zip_filename, 
#                                      filename=filename)
#         msg = MIMEMultipart()
        
#         if text:
#             msg.attach(MIMEText(text, 'plain'))

#         with open(zip_path, 'rb') as attachment:
#             part = MIMEBase('application', 'zip')
#             part.set_payload(attachment.read())
#             encoders.encode_base64(part)
#             part.add_header('Content-Disposition', f'attachment; filename="{zip_filename}"')
#             msg.attach(part)

#         file_manager.delete_obj(file_name=filename, bucket_name='evin-temp')
#         os.remove(zip_path)
#         return msg.as_string()
#     except Exception as error:
#         raise ValueError(f'Проблема с отправкой email: {error}')



# def get_email_template_files(email:str,filenames:list,type:str):
#     text = "The zip file contains both processed and raw files."
#     try:
#         msg = MIMEMultipart()
#         msg["Subject"] = 'Files have been processed'       
#         msg["From"] = f'SPD {EMAIL_SEND}' 
#         msg["To"] = email
        
#         filename='arch.zip'
#         file_manager=FileManager()
        
#         if type=='from_dir':
#             path_filename_files=file_manager.extract_files_from_trash_dir(filenames)
#             path_new_created_zf=file_manager.write_to_zip_file(path_filename_files=path_filename_files)                                    
#         if type=='from_zf':
#             path_filename_files=file_manager.extract_files_from_zf(filenames)
#             path_new_created_zf=file_manager.create_unique_temp_zipFile()
#         if not path_filename_files:
#             os.remove(path_new_created_zf)
#             return None
        
#         if text:
#             msg.attach(MIMEText(text))

#         with open(path_new_created_zf,'rb') as attachment:
#             part=MIMEBase('attachment','zip')
#             part.set_payload(attachment.read())
#             encoders.encode_base64(part)
#             part.add_header('content-disposition', 'attachment', filename=filename)
#             msg.attach(part)

#         os.remove(path_new_created_zf)
#         return msg.as_string()
#     except Exception as err:
#         print(f"{err}\nПроверь по внимательней явно что-то не так")
#         return None
    

# def get_email_template_files_debug(email:str,filename:str):
#     text = "The zip file contains both processed and raw files."
#     try:
#         msg = MIMEMultipart()
#         msg["Subject"] = 'Files have been processed'       
#         msg["From"] = f'SPD {EMAIL_SEND}' 
#         msg["To"] = email
        
#         zip_filename='arch.zip'
#         file_manager=FileManagerDebug()
#         zip_path = file_manager.create_zip_file(filename=filename, zipfilename=zip_filename)

#         if text: msg.attach(MIMEText(text))

#         with open(zip_path, 'rb') as attachment:
#             part = MIMEBase('application', 'zip')
#             part.set_payload(attachment.read())
#             encoders.encode_base64(part)
#             part.add_header(
#                 'Content-Disposition',
#                 f'attachment; filename="{os.path.basename(zip_filename)}"',
#             )
#             msg.attach(part)
#         os.remove(zip_path)
#         return msg.as_string()
#     except Exception as err:
#         raise ValueError(f"{err}\nПроверь по внимательней явно что-то не так")