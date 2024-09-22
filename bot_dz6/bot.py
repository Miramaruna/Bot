from bs4 import BeautifulSoup
import aiohttp
import asyncio
import logging
import sqlite3
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN


def init_db():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            news TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: Message):
    rates = await parsing_barmak()
    await message.answer(f"Добро пожаловать! Сейчас я покажу вам курсы валют:\n{rates}")

async def parsing_barmak():
    async with aiohttp.ClientSession() as session:
        async with session.get(url="https://www.nbkr.kg/index.jsp?lang=RUS") as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            block = soup.find('div', class_='exchange-rates block')
            
            if block:
                rows = block.find_all('tr')
                rates = []
                for row in rows[1:]: 
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        currency = cols[0].text.strip()
                        rate = cols[1].text.strip()
                        rates.append(f"{currency}: {rate}")
                return "\n".join(rates)
            else:
                return "Блок с курсами валют не найден."

@dp.message(Command('news'))
async def news_command(message: Message):
    await fetch_news(message)

async def fetch_news(message: Message):
    url = 'https://24.kg/'  
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')

            links = soup.find_all('a')
            news_links = []

            for link in links:
                href = link.get('href')  
                if href and href.startswith('/'):  
                    full_url = f'https://24.kg{href}'  
                    news_links.append(full_url)
                    save_news_to_db(full_url)

            if news_links:
                
                message_text = "\n".join(news_links)
                if len(message_text) > 4096:
                    message_text = message_text[:4093] + "..."
                await message.answer(message_text)
            else:
                await message.answer("Новостей не найдено.")

def save_news_to_db(news_text):
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO news (news) VALUES (?)", (news_text,))
    conn.commit()
    conn.close()

async def main():
    logging.basicConfig(level=logging.INFO)
    init_db()  
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")