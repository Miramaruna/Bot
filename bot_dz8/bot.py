from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, BotCommand
from config import TOKEN
import requests, time, asyncio, logging, aioschedule 
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ContentType
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import asyncio, aiogram, asyncio
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import aiogram, sqlite3, random, aioschedule

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

c = sqlite3.connect("bb.db")
cur = c.cursor()

cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER,
        name VARCHAR(30) NOT NULL,
        id_chat INTEGER NOT NULL,
        is_admin BOOLEAN NOT NULL
    )
""")

button_start = [
    [KeyboardButton(text='/mailing')],
    [KeyboardButton(text='/users')],
    [KeyboardButton(text='/register')]
]

st = ReplyKeyboardMarkup(keyboard=button_start, resize_keyboard=True)

button_admin = [
    [InlineKeyboardButton(text='add_admin', callback_data='ad')],
    [InlineKeyboardButton(text='delete_admin', callback_data='de')]
]

ad = InlineKeyboardMarkup(inline_keyboard=button_admin)

@dp.message(Command("start"))
async def start(message: Message):
    await message.reply("Это бот", reply_markup=st)

@dp.message(Command("register"))
async def register(message: Message):
    cur.execute(f"SELECT user_id FROM users WHERE user_id = {message.from_user.id}")
    d= cur.fetchall()
    if d==[]:
        cur.execute("INSERT INTO users(user_id, name, id_chat, is_admin) VALUES(?, ?, ?, ?)", (message.from_user.id, message.from_user.first_name, message.chat.id, False))
        c.commit()
        await message.reply("Вы зарегестрированы")
    else:
        await message.reply("Вы уже зарегистрированы")

class BroadcastForm(StatesGroup):
    waiting_for_message = State()

def get_all_users():
    conn = sqlite3.connect('bb.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    
    conn.close()
    return [user[0] for user in users]

async def broadcast_message(message_text):
    users = get_all_users()
    for user_id in users:
        try:
            await bot.send_message(chat_id=user_id, text=message_text)
        except TelegramBadRequest as e:
            print(f"Ошибка отправки пользователю {user_id}: {e}")

@dp.message(Command("mailing"))
async def start_broadcast(message: Message, state: FSMContext):
    cur.execute(f"SELECT is_admin FROM users WHERE user_id = {message.from_user.id}")
    adminy = cur.fetchone()
    c.commit()
    print(adminy)
    if adminy == 1:
        await message.answer("Введите сообщение для рассылки:")
        await state.set_state(BroadcastForm.waiting_for_message)
    else:
        await message.answer("У вас нет прав для выполнения этой команды.")

@dp.message(BroadcastForm.waiting_for_message, F.content_type == ContentType.TEXT)
async def get_broadcast_message(message: Message, state: FSMContext):
    broadcast_text = message.text

    await broadcast_message(broadcast_text)
    
    await message.answer("Рассылка завершена.")
    await state.clear()

@dp.message(Command("users"))
async def users(message: Message):
    cur.execute("SELECT name FROM users")
    user = cur.fetchall()
    if user:
        response = "список всех пользователей:\n"
        for users in user:
            users = user
            response += f"{users}\n"
    await message.reply(f"{response}", reply_markup=ad)

@dp.callback_query(F.data == 'ad')
async def add(callback: CallbackQuery):
    cur.execute(f"UPDATE users SET is_admin = 1 WHERE user_id = {callback.from_user.id}")
    c.commit()
    await callback.answer("add_admin")
    await callback.message.answer("Вы теперь админ")

@dp.callback_query(F.data == 'de')
async def de(callback: CallbackQuery):
    cur.execute(F"UPDATE users SET is_admin = 0 WHERE user_id {callback.from_user.id}")
    await callback.answer("de")
    await callback.message.answer("Вы теперь не админ")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
        
if __name__ == "__main__":
    asyncio.run(main())

# keyboard = ReplyKeyboardBuilder()
# for i in range(1,4):
#     keyboard.add(KeyboardButton(text=f'{i}'))
# await message.answer("Выберите число: ", reply_markup=keyboard.as_markup(resize_keyboard=True))
# await message.delete()  

# class Students(StatesGroup):
#     first_name = State()
#     last_name = State()
#     phone = State()
#     direction = State()

# # @dp.message(Register.name)
# async def register(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await message.reply("pon")

# name = data['Enail']
# await state.get_data()
# await state.clear()