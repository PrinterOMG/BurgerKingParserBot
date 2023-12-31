from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils import markdown as md

from tgbot.keyboards import inline_keyboards
from tgbot.misc import messages
from tgbot.services.bk_parser.parser import BurgerKingParser, AuthError, ApiError
from tgbot.services.database.models import TelegramUser


async def command_start(message: Message):
    db = message.bot.get('database')
    async with db() as session:
        tg_user = await session.get(TelegramUser, message.from_id)

        if tg_user is None:
            tg_user = TelegramUser(telegram_id=message.from_id)
            session.add(tg_user)
            await session.commit()

        await session.refresh(tg_user, ['bk_user'])
        if tg_user.bk_user is None:
            await message.answer(messages.start, reply_markup=inline_keyboards.start)
        else:
            await message.answer(messages.hello.format(username=tg_user.bk_user.name))


async def command_profile(message: Message):
    db = message.bot.get('database')

    async with db() as session:
        tg_user = await session.get(TelegramUser, message.from_id)
        await session.refresh(tg_user, ['bk_user'])
        bk_user = tg_user.bk_user
        await session.refresh(bk_user, ['city', 'restaurants'])

    await message.answer(messages.profile.format(
        name=bk_user.name,
        phone=bk_user.phone,
        city=bk_user.city.name,
        restaurants='\n'.join([rest.address for rest in bk_user.restaurants]),
        mailing='Включена' if bk_user.mailing else 'Выключена'
    ), reply_markup=inline_keyboards.profile)


async def command_help(message: Message):
    await message.answer(messages.help_text, reply_markup=inline_keyboards.contact)


async def command_news(message: Message):
    await message.answer(messages.news, reply_markup=inline_keyboards.contact)


async def commands_checks(message: Message):
    db = message.bot.get('database')

    async with db() as session:
        tg_user = await session.get(TelegramUser, message.from_id)
        await session.refresh(tg_user, ['bk_user'])
        bk_user = tg_user.bk_user
        await session.refresh(bk_user, ['restaurants'])

        text = ''
        bk_parser = BurgerKingParser(bk_user.token)
        for rest in bk_user.restaurants:
            text += f'\n\n{md.hbold(rest.address)}'
            try:
                dates = await bk_parser.parse_restaurant_dates(rest.id)
            except AuthError:
                await message.answer(messages.auth_error, reply_markup=inline_keyboards.relogin)
                bk_user.mailing = False
                return
            except ApiError:
                await message.answer(text=messages.api_error)
                bk_user.mailing = False
                return
            add = False
            for date in dates['dates']:
                if date['disabled']:
                    continue
                text += f'\n{md.hunderline(date["date"])}'
                for time in date['times']:
                    if time['disabled']:
                        continue
                    add = True
                    text += f'\n\tс {time["startTime"]} до {time["endTime"]}'
            if not add:
                text += '\nПусто :('

    await message.answer(text)


def register_commands(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], state='*')
    dp.register_message_handler(command_profile, commands=['profile'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(command_news, commands=['news'])
    dp.register_message_handler(commands_checks, commands=['checks'])
