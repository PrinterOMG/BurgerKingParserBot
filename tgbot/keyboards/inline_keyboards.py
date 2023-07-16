from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc import callbacks


start = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('🌐 BurgerKing', url='https://burgerkingrus.ru/proverka/account/')
    ],
    [
        InlineKeyboardButton('Начать вход', callback_data='start_login')
    ]
])

profile = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('Вкл/выкл рассылку', callback_data='switch_mailing')
    ]
])

relogin = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('Войти повторно', callback_data='relogin')
    ]
])

contact = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('Связаться', url='t.me/printeromg')
    ]
])
