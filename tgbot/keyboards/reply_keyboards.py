from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.misc import reply_commands


contact_request = ReplyKeyboardMarkup([
    [
        KeyboardButton(reply_commands.share_contact, request_contact=True)
    ]
], resize_keyboard=True)

code_input = ReplyKeyboardMarkup([
    [
        KeyboardButton(reply_commands.new_phone_request)
    ],
    [
        KeyboardButton(reply_commands.new_code_request)
    ]
], resize_keyboard=True)
