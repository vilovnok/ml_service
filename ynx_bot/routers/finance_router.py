from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import time
from datetime import datetime, timedelta

router = Router()
router.name = 'finance'


@router.message(Command('balance'))
async def check_balance(message: Message):

    user_id = message.from_user.id
    user_name = message.from_user.full_name
    
    mock_balance = 500
    
    balance_text = f"💰 {user_name}, ваш текущий баланс: {mock_balance} YNX"
    await message.answer(balance_text)



@router.message(Command('credit'))
async def issue_credit(message: Message):
    await message.answer('🏦 Пожалуйста, подождите. Проверяем вашу кредитную историю...')
    
    time.sleep(3)    
    user_name = message.from_user.full_name
    credit_amount = 500
    
    credit_text = (
        f"✅ Уважаемый {user_name}!\n"
        f"Вам одобрен кредит на сумму {credit_amount} YNX\n"
        "Условия кредита:\n"
        "- Срок: 30 дней\n"
        "- Процентная ставка: 5%\n"
        "Для подтверждения получения кредита ответьте 'Подтверждаю'"
    )
    await message.answer(credit_text)



@router.message(Command('history'))
async def transaction_history(message: Message):
    user_name = message.from_user.full_name
    
    current_time = datetime.now()    
    history_text = f"📊 История транзакций для {user_name}:\n\n"
    
    transactions = [
        {
            'date': current_time - timedelta(days=1),
            'type': '💸 Кредит получен',
            'amount': '+500 YNX'
        },
        {
            'date': current_time - timedelta(days=2),
            'type': '💳 Оплата',
            'amount': '-200 YNX'
        },
        {
            'date': current_time - timedelta(days=3),
            'type': '💰 Пополнение',
            'amount': '+1000 YNX'
        }
    ]
    
    for tx in transactions:
        history_text += f"📅 {tx['date'].strftime('%d.%m.%Y %H:%M')}\n"
        history_text += f"{tx['type']}: {tx['amount']}\n"
        history_text += "─────────────────\n"
    
    await message.answer(history_text)
