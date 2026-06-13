import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8682146115:AAHSRT_UT6mpMCzI6WkF4fqHKFcwqOPii9k"
CHANNEL_ID = -1003903740959
MINI_APP_URL = "https://neuro-sport-sight.base44.app"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    is_subscribed = await check_subscription(user_id)
    if is_subscribed:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("🤖 Открыть MatchGPT", web_app=types.WebAppInfo(url=MINI_APP_URL)))
        await message.answer("✅ Добро пожаловать! Нажми кнопку:", reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("📢 Подписаться на канал", url="https://t.me/+azG9xVm4b21mODcy"))
        keyboard.add(InlineKeyboardButton("✅ Я подписался", callback_data="check_sub"))
        await message.answer("👋 Привет! Подпишись на канал для доступа:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "check_sub")
async def check_sub_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    is_subscribed = await check_subscription(user_id)
    if is_subscribed:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("🤖 Открыть MatchGPT", web_app=types.WebAppInfo(url=MINI_APP_URL)))
        await callback.message.answer("✅ Отлично! Теперь у тебя есть доступ:", reply_markup=keyboard)
    else:
        await callback.answer("❌ Ты ещё не подписался на канал!", show_alert=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
