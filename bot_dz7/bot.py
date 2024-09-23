from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, BotCommand
from config import TOKEN
import requests, time, asyncio, logging, aioschedule 

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_monitoring.log'),  
        logging.StreamHandler() 
    ]
)

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

monitoring = False
monitoring_ech = False
monitoring_ltc = False
chat_id = None


async def get_btc_price():
    url = 'https://api.binance.com/api/v3/avgPrice?symbol=BTCUSDT'
    response = requests.get(url=url).json()
    price = response.get('price')
    if price:
        return f'Стоимость биткоина на {time.ctime()}, {price}'
    else:
        return f'Не удалось получить цену биткоина'

async def monitor_btc_price():
    global monitoring
    while monitoring:
        message = await get_btc_price()
        await bot.send_message(chat_id, message)
        await asyncio.sleep(10)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}')

@dp.message(Command('btc'))
async def btc(message: Message):
    global chat_id, monitoring
    chat_id = message.chat.id
    if not monitoring:
        monitoring = True
        await message.answer("Начало мониторинга биткоина")
        asyncio.create_task(monitor_btc_price())
        await message.answer("Мониторинг уже запущен!")


async def get_ech_price():
     url = 'https://api.binance.com/api/v3/avgPrice?symbol=ETHUSDT'
     response = requests.get(url=url).json()
     price = response.get('price')
     if price:
         return f'Стоимость Ethereum на {time.ctime()}, {price}'
     else:
         return f'Не удалось получить цену Ethereum'

async def monitor_eth_price():
    global monitoring_ech
    while monitoring_ech:
        message = await get_ech_price()
        await bot.send_message(chat_id, message)
        await asyncio.sleep(10)

@dp.message(Command("ech"))
async def ech(message: Message):
    global chat_id, monitoring_ech
    chat_id = message.chat.id
    if not monitoring_ech:
        monitoring_ech = True
        await message.answer("Начало мониторинга Ethereum")
        asyncio.create_task(monitor_eth_price())

async def get_ltc_price():
    url = 'https://api.binance.com/api/v3/avgPrice?symbol=LTCUSDT'
    response = requests.get(url=url).json()
    price = response.get('price')
    if price:
        return f'Стоимость Litecoin на {time.ctime()}, {price}'
    else:
        return f'Не удалось получить цену Litecoin'

async def monitor_ltc_price():
    global monitoring_ltc
    while monitoring_ltc:
        message = await get_ltc_price()
        await bot.send_message(chat_id, message)
        await asyncio.sleep(10)

@dp.message(Command("ltc"))
async def ltc(message: Message):
    global chat_id, monitoring_ltc
    chat_id = message.chat.id
    if not monitoring_ltc:
        monitoring_ltc = True
        await message.answer("Начало мониторинга Litecoin")
        asyncio.create_task(monitor_ltc_price())


@dp.message(Command('stop'))
async def main_stop(message: Message):
    global monitoring, monitoring_ech, monitoring_ltc
    sttop = False

    if monitoring:
        monitoring = False
        sttop = True
        await message.answer('Мониторинг биткоина остановлен')

    if monitoring_ech:
        monitoring_ech = False
        sttop = True
        await message.answer('Мониторинг Ethereum остановлен')

    if monitoring_ltc:
        monitoring_ltc = False
        sttop = True
        await message.answer('Мониторинг Litecoin остановлен')

    if not sttop:
        await message.answer('Мониторинг уже остановлен')

async def through():
    while True:
        if monitoring or monitoring_ech or monitoring_ltc:
            if monitoring:
                message = await get_btc_price()
                await bot.send_message(chat_id, message)    
           
            if monitoring_ech:
                message = await get_ech_price()
                await bot.send_message(chat_id, message)
            
            if monitoring_ltc:
                message = await get_ltc_price()
                await bot.send_message(chat_id, message)
            
            await asyncio.sleep(600) 
        else:
            logging.info("Мониторинг не запущен")
            await asyncio.sleep(60)  


async def on_startup():
    await bot.set_my_commands([
        BotCommand(command="/start", description='Запустить бота'),
        BotCommand(command="/btc", description='Начать мониторинг BTC'),
        BotCommand(command="/ech", description='Начало мониторинга ETH'),
        BotCommand(command="/ltc", description='Начало мониторинга LTC'),
        BotCommand(command="/stop", description='Остановить мониторинг')
    ])
    logging.info("БОТ ЗАПУЩЕН")

async def main():
    
    await on_startup()
    asyncio.create_task(through())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def proverka():
    try:
        await bot.send_message(chat_id, "Проверка бота")
        logging.info("Бот работает")
        await asyncio.sleep(1000)
    except Exception as e:
        logging.error(f"Ошибка во время проверки бота: {e}")
        await asyncio.sleep(60)
        await proverka()
        
if __name__ == "__main__":
    asyncio.run(main())