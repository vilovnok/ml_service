from sqlalchemy.ext.asyncio  import create_async_engine
from sqlalchemy.exc import OperationalError
import asyncio

db_url = "postgresql+asyncpg://postgres:1234@localhost:5555/ynix-db"
engine = create_async_engine(db_url)

async def check_connection():
    try:
        async with engine.connect() as connection:
            print("Соединение с базой данных успешно установлено.")
    except OperationalError as e:
        print(f"Не удалось подключиться к базе данных: {e}")

asyncio.run(check_connection())