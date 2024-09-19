# sqlite3

import sqlite3, random

# aiogram

from aiogram import F, Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.keyboards import *

router = Router()

conn = sqlite3.connect('Bank.db')
cur = conn.cursor()

cur.execute("""
               CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY,
               first_name VARCHAR(30),
               balance INTEGER
               )
               """)

@router.message(Command("start"))
async def start(message: Message):
    await message.reply("Привет это бот Банк")

@router.message(Command("add"))
async def add (message: Message):
    cur.execute(f"UPDATE users SET balance = balance + ? WHERE id = ?", (2000, message.from_user.id))
    conn.commit()
    await message.reply("Деньги начислены")

@router.message(Command("info"))
async def info(message: Message):
    cur.execute(f"SELECT balance FROM users WHERE id = {message.from_user.id}")
    balance = cur.fetchall()
    cur.execute(f"SELECT id FROM users WHERE id = {message.from_user.id}")
    id = cur.fetchall()
    conn.commit()
    await message.reply(f"Имя - {message.from_user.first_name}\nID - {id} \nБаланс - {balance}")

@router.message(Command("register"))
async def register(message: Message):
    cur.execute(f"SELECT id FROM users WHERE id = {message.from_user.id}")
    admin = cur.fetchall()
    if admin == []:
        cur.execute("INSERT INTO users VALUES (?, ?, ?)", (message.from_user.id, message.from_user.first_name, 500))
        conn.commit()
        await message.reply("Регистрация выполнена")
    else:
        await message.reply("Акааунт уже существует")

@router.message(Command("users"))
async def users(message: Message):
    cur.execute(f"SELECT first_name, id FROM users")
    useri = cur.fetchall()
    conn.commit()
    if useri:
        response = "список всех пользователей:\n"
        for user_id, users in useri:
            users = useri
            response += f"{user_id}. {users}\n"
    await message.reply(f"{response}")

@router.message(Command('transfer'))
async def transfer_pol(message: Message):

    try:
        args = message.text.split()
        if len(args) < 3:
            raise ValueError("Неверный формат команды. Используйте: /transfer <id получателя> <сумма> Пример /transfer id пользавателя 100")

        receiver_id = int(args[1])
        amount = float(args[2])

        cur.execute("SELECT balance FROM users WHERE id = ?", (message.from_user.id,))
        sender_balance = cur.fetchone()

        if sender_balance is None:
            raise ValueError("Пользователь-отправитель не найден")
        
        if sender_balance[0] < amount:
            raise ValueError("Недостаточно средств для перевода")

        cur.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, message.from_user.id))
        cur.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, receiver_id))

        conn.commit()
        await message.reply("Перевод выполнен успешно")

    except Exception as e:
        conn.rollback()
        await message.reply(f"Ошибка: {e}")