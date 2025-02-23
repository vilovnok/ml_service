from aiogram import Router, F
from .dependencies import UOWDep
from aiogram.filters import Command
from aiogram.types import Message
from ynx_bot.services.register import *


router = Router()
router.name = 'welcome'


@router.message(Command('start'))
async def cmd_start(message: Message, uow=UOWDep):

    user_id = message.from_user.id 
    user_name = message.from_user.full_name

    result = await RegisterServices().get_one(uow=uow, user_id=user_id)
    # result = await connect2db(uow=uow, user_id=user_id)

    # result = await uow.register.get_one(id=user_id, n_tab=0)
    
    welcome_text = (
        '🏦 Добро пожаловать в Yanix Trade — инновационную торговую систему, где валютой являются Яниксы (Инь и Ян)!\n\n'
        '💡 Я помогу Вам:\n'
        '- Пополнять счет и управлять балансом\n'
        '- Получать быстрые кредиты\n'
        '- Отслеживать историю транзакций\n\n'
        '📝 Доступные команды:\n'
        '/balance - проверить баланс\n'
        '/credit - получить кредит\n'
        '/history - история транзакций\n\n'
        f'{user_id} {user_name}\n\n'
        f'{result}\n\n'
    )

    
    return await message.answer(welcome_text)


# @router.message(F.text)
# async def handle_text(message: Message):
#     help_text = (
#         "⚠️ Пожалуйста, используйте доступные команды:\n"
#         "/balance - проверить баланс\n"
#         "/credit - получить кредит\n"
#         "/history - история транзакций\n\n"
#     )
#     await message.answer(help_text) 