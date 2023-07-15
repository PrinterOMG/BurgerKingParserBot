from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.misc import messages
from tgbot.services.database.models import TelegramUser


async def command_start(message: Message):
    db = message.bot.get('database')
    async with db() as session:
        tg_user = await session.get(TelegramUser, message.from_id)
        if tg_user is None:
            new_user = TelegramUser(telegram_id=message.from_id)
            session.add(new_user)
            await session.commit()
    await message.reply(messages.hello.format(username=message.from_user.username))


def register_commands(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], state='*')
