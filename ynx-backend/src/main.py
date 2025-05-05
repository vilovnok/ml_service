from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi import Request
from time import time
from redis import asyncio as aioredis

from api.routers import all_routers
from config import REDIS_HOST, REDIS_PORT

from logging_config import logger



app = FastAPI(title='RestAPI')
origins = ["http://localhost:4200","http://localhost:80"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin","Authorization"],
)

for router in all_routers:
    app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 FastAPI запущен")
    try:
        redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        logger.info("🔌 Redis кэш инициализирован")
    except Exception as err:
        logger.error(f"Ошибка подключения Redis: {err}")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = round(time() - start_time, 4)

    client_ip = request.client.host
    logger.info(
        f"{client_ip} - {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time}s"
    )
    return response