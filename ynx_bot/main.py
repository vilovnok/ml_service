import asyncio
from aiogram import Bot, Dispatcher
import hydra
from omegaconf import DictConfig

from ynx_bot.routers.welcome_router import router as welcome_router
from ynx_bot.routers.finance_router import router as finance_router

async def start_bot(token: str) -> None:
    bot = Bot(token=token)
    dp = Dispatcher()
    
    dp.include_router(welcome_router)
    dp.include_router(finance_router)
    
    print('____START____')
    await dp.start_polling(
        bot, 
        allowed_updates=dp.resolve_used_update_types(),
    )

@hydra.main(version_base=None, config_path=".", config_name="config")
def main(cfg: DictConfig) -> None:
    token = cfg.ynx_bot.token
    asyncio.run(start_bot(token))

if __name__ == "__main__":
    main()