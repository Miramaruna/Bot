import asyncio, aiogram

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from app.keyboards import *

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.reply("Привет!", reply_markup=keyboard_start)

@router.message(F.text == "Направления")
async def direction(message: Message):
    await message.answer("Вот все направления:", reply_markup=inline_direction_keyboard)

@router.callback_query(F.data == 'front')
async def front(callback: CallbackQuery):
    await callback.answer("Вы выбрали Frontend")
    await callback.message.edit_text("Вы выбрали направление Frontend",reply_markup=front_keyboard)

    @router.callback_query(F.data == 'cs')
    async def cs(callback: CallbackQuery):
        await callback.answer("Вы выбрали CSS")
        await callback.message.edit_text("CSS (Cascading Style Sheets) — это язык стилей, используемый для оформления и управления визуальным представлением веб-страниц, созданных с помощью HTML. CSS позволяет отделить содержимое (HTML) от его представления, что упрощает создание и поддержание стиля веб-сайтов.")

    @router.callback_query(F.data == 'html')
    async def html(callback: CallbackQuery):
        await callback.answer("Вы выбрали HTML")
        await callback.message.edit_text("HTML (HyperText Markup Language) — это язык разметки, используемый для создания и структурирования веб-страниц. HTML определяет структуру контента на веб-странице с помощью различных тегов и атрибутов. Веб-браузеры интерпретируют HTML-код и отображают его в виде веб-страниц, которые вы видите в интернете.")

    @router.callback_query(F.data == 'js')
    async def js(callback: CallbackQuery):
        await callback.answer("Вы выбрали JS")
        await callback.message.edit_text("JavaScript (JS) — это высокоуровневый, интерпретируемый язык программирования, который используется для создания динамичного и интерактивного контента на веб-страницах. Он позволяет веб-разработчикам добавлять функциональность, такую как анимация, обработка событий, взаимодействие с сервером и многое другое.")

@router.callback_query(F.data == "back")
async def backend(callback: CallbackQuery):
    await callback.answer("Вы выбрали Backend")
    await callback.message.edit_text("Вы выбрали направление Backend", reply_markup=back_keyboard)

    @router.callback_query(F.data == 'py')
    async def py(callback: CallbackQuery):
        await callback.answer("Вы выбрали Python")
        await callback.message.edit_text("Python — это высокоуровневый, интерпретируемый язык программирования, который широко используется благодаря своей простоте, читаемости и универсальности. Он был создан Гвидо ван Россумом и впервые выпущен в 1991 году. Python подходит для решения множества задач, от веб-разработки и автоматизации до анализа данных и машинного обучения.")

    @router.callback_query(F.data == 'ai')
    async def ai(callback: CallbackQuery):
        await callback.answer("вы выбрали Aiogram")
        await callback.message.edit_text("aiogram — это популярная асинхронная библиотека для создания ботов в Telegram на языке программирования Python. Она основана на aiohttp и предназначена для работы с Telegram Bot API в асинхронном режиме, что позволяет создавать высокопроизводительные и масштабируемые боты.")

    @router.callback_query(F.data == 'dj')
    async def dj(callback: CallbackQuery):
        await callback.answer("Вы выбрали Django")
        await callback.message.edit_text("Django — это высокоуровневый фреймворк для веб-разработки на языке Python, который упрощает создание сложных, базирующихся на базе данных веб-приложений. Django следует принципам DRY (Don't Repeat Yourself) и батарейки в комплекте batteries-included, что означает, что он предоставляет множество встроенных функций и инструментов для быстрого и эффективного разработки веб-приложений.")

@router.callback_query(F.data == 'android')
async def andr(callback: CallbackQuery):
    await callback.answer("Вы выбрали Android")
    await callback.message.edit_text("Вы выбрали направление Android", reply_markup=android_keyboard)

@router.callback_query(F.data == 'ux')
async def ux(callback: CallbackQuery):
    await callback.answer("Вы выбрали Дизайн")
    await callback.message.edit_text("Вы выбрали направление Дизайн", reply_markup=ux_keyboard)

