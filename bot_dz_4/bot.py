import aiogram, logging, asyncio

from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from config import TOKEN
from app.handlers import *

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

# start

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")