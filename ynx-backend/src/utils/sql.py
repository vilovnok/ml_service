import psycopg2
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

def conn_to_db():
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    conn = psycopg2.connect(DATABASE_URL)    
    return conn  
        