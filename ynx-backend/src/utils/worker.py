import smtplib
from config import *
from utils.mail import *
from celery import Celery
from models.generate import *
from utils.model import chat_fun, topUp_fun
from utils.sql import conn_to_db

from datetime import datetime
from zoneinfo import ZoneInfo


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


@celery.task
def generate_text(user_id: int, message: str, token: str):
    query_message_gen = f"""
                UPDATE account 
                SET balance = balance - 10
                WHERE user_id = %s;
            """
    query_update_completed = f"""
                UPDATE request 
                SET status = 'completed', message_gen = %s, finished_at = %s
                WHERE token = %s;
            """
    
    query_update_failure = f"""
                UPDATE request 
                SET status = 'failed', message_gen = %s, finished_at = %s
                WHERE token = %s;
            """
    try:
        conn = conn_to_db()
        cursor = conn.cursor() 
        finished_at = datetime.now(ZoneInfo("Europe/Moscow"))
        message_gen = chat_fun(message=message)
        cursor.execute(query_message_gen, (user_id,))
        cursor.execute(query_update_completed, (message_gen, finished_at, token))
        conn.commit()       
    except Exception as e:
        cursor.execute(query_update_failure, ('nan', finished_at, token))
        conn.commit()       
        print(f"Error(generate task):\n\n{e}\n\n")
    finally:
       if conn:
           cursor.close()            


@celery.task
def topUpBalance(user_id: int, message: str, token: str):
    query_top_up_balance = f"""
                UPDATE account 
                SET balance = balance + %s
                WHERE user_id = %s;
            """
    query_update_completed = f"""
                UPDATE request_security
                SET status = 'completed', message_gen = %s, finished_at = %s
                WHERE token = %s;
            """    
    query_update_failure = f"""
                UPDATE request_security 
                SET status = 'failed', message_gen = %s, finished_at = %s
                WHERE token = %s;
            """
    
    try:
        conn = conn_to_db()
        cursor = conn.cursor()         
        finished_at = datetime.now(ZoneInfo("Europe/Moscow"))
        message_gen = topUp_fun(message=message)
        message_gen = message_gen[0]['label']
        
        if message_gen=='убедил':
            cursor.execute(query_update_completed, (message_gen, finished_at, token))            
            cursor.execute(query_top_up_balance, (10, user_id))
            conn.commit()
        else:
            cursor.execute(query_update_completed, (message_gen, finished_at, token))
            cursor.execute(query_top_up_balance, (0, user_id))
            conn.commit()
    except Exception as e:
        cursor.execute(query_update_failure, ('nan', finished_at, token))
        conn.commit()       
        print(f"Error(top up balance):\n\n{e}\n\n")
    finally:
       if conn:
           cursor.close()            


