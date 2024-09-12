from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

button_start = [
    [KeyboardButton(text="Направления")]
]

keyboard_start = ReplyKeyboardMarkup(keyboard=button_start, resize_keyboard=True)

inline_direction = [
    [InlineKeyboardButton(text="Frontend", callback_data='front'),
     InlineKeyboardButton(text="Backend", callback_data='back'),
     InlineKeyboardButton(text='UX/UI', callback_data='ux'),
     InlineKeyboardButton(text='Android', callback_data='android')]
]

inline_direction_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_direction)

front = [
    [InlineKeyboardButton(text="html", callback_data='html'), InlineKeyboardButton(text="css", callback_data='cs'),
    InlineKeyboardButton(text="js", callback_data='js')]
]

front_keyboard = InlineKeyboardMarkup(inline_keyboard=front)

back = [
    [InlineKeyboardButton(text='Python', callback_data='py'),
     InlineKeyboardButton(text='Django', callback_data='dj'),
     InlineKeyboardButton(text='Aiogram', callback_data='ai')]
]

back_keyboard = InlineKeyboardMarkup(inline_keyboard=back)

android_inline = [
    [InlineKeyboardButton(text="Java and Kotlin", url='https://docs.oracle.com/en/java/'), 
    InlineKeyboardButton(text='Android Studio', url='https://developer.android.com/studio/intro?hl=ru'),
    InlineKeyboardButton(text='Jetpack', url='https://developer.android.com/jetpack?hl=ru')]
]
android_keyboard = InlineKeyboardMarkup(inline_keyboard=android_inline)

ux_inline = [
    [InlineKeyboardButton(text='Figma', url='https://www.reg.ru/blog/zhutkie-sajty-kotorye-vyzovut-u-vas-murashki/'), 
    InlineKeyboardButton(text='Sketch', url='https://www.reg.ru/blog/zhutkie-sajty-kotorye-vyzovut-u-vas-murashki/'), 
    InlineKeyboardButton(text='Framer', url='https://www.reg.ru/blog/zhutkie-sajty-kotorye-vyzovut-u-vas-murashki/')]
]
ux_keyboard = InlineKeyboardMarkup(inline_keyboard=ux_inline)