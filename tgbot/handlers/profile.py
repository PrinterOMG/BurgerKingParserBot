from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from tgbot.keyboards import inline_keyboards
from tgbot.misc import messages
from tgbot.services.database.models import TelegramUser


async def show_profile(call: CallbackQuery):
    db = call.bot.get('database')

    async with db() as session:
        tg_user = await session.get(TelegramUser, call.from_user.id)
        await session.refresh(tg_user, ['bk_user'])
        bk_user = tg_user.bk_user
        await session.refresh(bk_user, ['city', 'restaurants'])

    await call.message.edit_text(messages.profile.format(
        name=bk_user.name,
        phone=bk_user.phone,
        city=bk_user.city.name,
        restaurants='\n'.join([rest.address for rest in bk_user.restaurants]),
        mailing='Включена' if bk_user.mailing else 'Выключена'
    ), reply_markup=inline_keyboards.profile)
    await call.answer()


async def switch_mailing(call: CallbackQuery):
    db = call.bot.get('database')

    async with db() as session:
        tg_user = await session.get(TelegramUser, call.from_user.id)
        await session.refresh(tg_user, ['bk_user'])
        bk_user = tg_user.bk_user
        bk_user.mailing = not bk_user.mailing
        await session.commit()

    await show_profile(call)


def register_profile(dp: Dispatcher):
    dp.register_callback_query_handler(switch_mailing, text='switch_mailing')
