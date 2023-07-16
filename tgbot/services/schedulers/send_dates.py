import asyncio
import datetime
import logging
from pprint import pprint

import aioredis
from aiogram import Bot
from aiogram.dispatcher import FSMContext
from sqlalchemy import select

from tgbot.keyboards import inline_keyboards
from tgbot.misc import messages
from tgbot.services.bk_parser.parser import BurgerKingParser, AuthError, ApiError
from tgbot.services.database.models import BKUser, SavedDate


async def send_dates(bot: Bot, db):
    stmt = select(BKUser).where(BKUser.mailing == True)
    bk_parser = BurgerKingParser()
    async with db.begin() as session:
        records = await session.execute(stmt)
        users = records.scalars().all()

        for user in users:
            bk_parser.update_token(user.token)
            await session.refresh(user, ['restaurants', 'saved_dates'])
            for rest in user.restaurants:
                try:
                    rest_dates = await bk_parser.parse_restaurant_dates(rest.id)
                except AuthError:
                    await bot.send_message(chat_id=user.telegram_id, text=messages.auth_error,
                                           reply_markup=inline_keyboards.relogin)
                    user.mailing = False
                    continue
                except ApiError:
                    await bot.send_message(chat_id=user.telegram_id, text=messages.api_error)
                    user.mailing = False
                    continue

                for rest_date in rest_dates['dates']:
                    date = datetime.datetime.strptime(rest_date['date'], '%d.%m.%Y').date()
                    if rest_date['disabled'] or is_date_in_saved_dates(date, user.saved_dates, rest.id):
                        continue
                    times = '\n'.join(f'c {time["startTime"]} до {time["endTime"]}' for time in rest_date['times'] if not time['disabled'])
                    text = messages.new_check.format(
                        address=rest.address,
                        date=rest_date['date'],
                        times=times
                    )
                    await bot.send_message(chat_id=user.telegram_id, text=text)
                    date = datetime.datetime.strptime(rest_date['date'], '%d.%m.%Y').date()
                    new_saved_date = SavedDate(date=date, restaurant_id=rest.id, bk_user_id=user.id)
                    session.add(new_saved_date)


def is_date_in_saved_dates(date, saved_dates, rest_id) -> bool:
    rest_saved_dates = filter(lambda s_date: s_date.restaurant_id == rest_id, saved_dates)
    for saved_date in rest_saved_dates:
        if date == saved_date.date:
            return True
    return False
