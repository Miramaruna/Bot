
# sqlite3

import sqlite3

# aiogram

import asyncio, logging, random

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# config

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

connection = sqlite3.connect("dz.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS dz(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    task TEXT
    )
""")

@dp.message(Command("start"))
async def start(message: Message):
    await message.reply("Привет!\nЯ бот для управления задачами\nИспользуй команду, add - чтоб добавить задачу, /view - чтоб увидеть все задачи, /delete - Что, удалить задачу")

async def save_message(user_id, task):
    conn = sqlite3.connect('DZ.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO dz (user_id, task)
        VALUES (?, ?)
    ''', (user_id, task))
    
    conn.commit()
    conn.close()

@dp.message(Command("view"))
async def view(message: Message):
    cursor.execute(f"SELECT id, task FROM dz WHERE user_id = {message.from_user.id}")
    view = cursor.fetchall()
    connection.commit()
    connection.close()
    await message.reply(f"Список задач:{view}")

@dp.message(Command("delete"))
async def delete(message: Message):
    cursor.execute("DELETE id, task FROM dz WHERE id = ?")

    

@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    task = message.text
    await save_message(user_id, task)
    await message.reply("Ваше сообщение сохранено!")

async def main():
    await dp.start_polling(bot)

# start

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")