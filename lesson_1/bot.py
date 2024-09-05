import asyncio
import logging
import random

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

button_start = [
    [KeyboardButton(text='/play'), KeyboardButton(text='/info'), KeyboardButton(text='/help')]
]

button_play = [
    [KeyboardButton(text='/1'), KeyboardButton(text='/2'), KeyboardButton(text='/3')]
]

button_info = [
    [KeyboardButton(text='/GEEKS')]
]

keyboard_start = ReplyKeyboardMarkup(keyboard=button_start, resize_keyboard=True)
keyboard_play = ReplyKeyboardMarkup(keyboard=button_play, resize_keyboard=True)
keyboard_info = ReplyKeyboardMarkup(keyboard=button_info, resize_keyboard=True)

# Version = 2.1.3
# home Replit
# UptimeRobot

@dp.message(Command("start"))
async def start_bot(message: Message):
    await message.reply(f"Привет {message.from_user.first_name}!\nЭто бот мируни\nТут все команды этого бота\nИграть! - /play\nПерезапуск бота - /start\nПомощь - /help\nИнформация - /info", reply_markup=keyboard_start)

@dp.message(Command("help"))
async def help(message: Message):
    await message.reply("Привет помочь?\nКоманда старта /start\nИнформация - /info \nЕсли нужна помощь обращяйся по это команде /help")

@dp.message(Command("play"))
async def play_bot(message: Message):
    await message.reply("Привет я загадал число от 1 до 3 отгадай число!" , reply_markup=keyboard_play)

@dp.message(Command("info"))
async def info(message: Message):
    await message.reply("Привет!\nЭто информация о моем боте\nМой бот обычные слова воспринимает как эхо тоесть он не будет повторять слова\nА будет писать значение по умолчанию как (pon)\nНа этом у меня все!\nУдачи!\n/start \nVersion == 2.1.3", reply_markup=keyboard_info)

@dp.message(Command("/GEEKS"))
async def info(message: Message):
    await message.answer('Научился я этому в учебном месте GEEKS это хорошое место для изучения программирования а также других сфер \nКак дизайн программирования для телефона и т.д\n/start', reply_markup=keyboard_start)

@dp.message(Command("1"))
async def odin(message: Message):
    if 1 == random.randint(1,3):
        await message.answer_photo(photo="https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg", caption="Ты выйграл!\n/start", reply_markup=keyboard_play)
    else:
        await message.answer_photo(photo="https://media.makeameme.org/created/sorry-you-lose.jpg", caption="Ты проиграл!\n/start", reply_markup=keyboard_play)
        
@dp.message(Command("2"))
async def dva(message: Message):
    if 2 == random.randint(1,3):
        await message.answer_photo(photo="https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg", caption="Ты выйграл!\n/start", reply_markup=keyboard_play)
    else:
        await message.answer_photo(photo="https://media.makeameme.org/created/sorry-you-lose.jpg", caption="Ты проиграл!\n/start", reply_markup=keyboard_play)

@dp.message(Command("3"))
async def tri(message: Message):
    if 3 == random.randint(1,3):
        await message.answer_photo(photo="https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg", caption="Ты выйграл!\n/start", reply_markup=keyboard_play)
    else:
        await message.answer_photo(photo="https://media.makeameme.org/created/sorry-you-lose.jpg", caption="Ты проиграл!\n/start", reply_markup=keyboard_play)

@dp.message()
async def echo(message: Message):
    await message.answer("pon")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")