from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

SECRET = os.environ.get('SECRET')
REFRESH_SECRET = os.environ.get('REFRESH_SECRET')
ALGORITHM = os.environ.get('ALGORITHM')

UPLOADS_DIR = os.environ.get('UPLOADS_DIR')

RABBITMQ_DEFAULT_USER=os.environ.get('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS=os.environ.get('RABBITMQ_DEFAULT_PASS')
RABBITMQ_DEFAULT_HOST=os.environ.get('RABBITMQ_DEFAULT_HOST')
RABBITMQ_DEFAULT_PORT=os.environ.get('RABBITMQ_DEFAULT_PORT')

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

EMAIL_SEND = os.environ.get('EMAIL_SEND')
EMAIL_PASS = os.environ.get('EMAIL_PASS')

SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')

HF_TOKEN = os.environ.get('HF_TOKEN')
MODEL_ID_CHAT = os.environ.get('MODEL_ID_CHAT')
MODEL_ID_CLS = os.environ.get('MODEL_ID_CLS')

FR_PORT = os.environ.get('FR_PORT')


