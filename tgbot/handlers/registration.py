import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import Message, ContentType, ReplyKeyboardRemove, CallbackQuery

from tgbot.keyboards import reply_keyboards
from tgbot.misc import states, messages, reply_commands
from tgbot.services.bk_parser.parser import BurgerKingParser, ApiError
from tgbot.services.database.models import BKUser, City, Restaurant


async def start_registration(call: CallbackQuery):
    await call.message.answer(messages.phone_input, reply_markup=reply_keyboards.contact_request)
    await states.Registration.first()
    await call.answer()


async def new_phone(message: Message):
    await message.answer(messages.phone_input, reply_markup=reply_keyboards.contact_request)
    await states.Registration.first()


async def new_code(message: Message, state: FSMContext):
    data = await state.get_data()
    phone = data['phone']
    await message.answer(messages.code_input.format(phone=phone), reply_markup=reply_keyboards.code_input)
    message.text = phone
    await get_user_phone(message, state)


async def check_result(result, message, state):
    if 'status' not in result:
        await message.answer(messages.something_went_wrong_with_api, reply_markup=ReplyKeyboardRemove())
        await state.finish()
        raise CancelHandler

    if result['status'] != 'ok':
        logging.error(result)
        await message.answer(messages.bad_phone.format(error=result['error']['message']))
        raise CancelHandler


async def get_user_phone(message: Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text.replace(' ', '').replace('(', '').replace(')', '').replace('+', '').replace('-', '')

    if not phone.isdigit() or len(phone) != 11 or not phone.startswith('7'):
        await message.answer(messages.bad_phone.format(error='Номер должен состоять из цифр и начинаться с "7"'))
        return

    bk_parser = BurgerKingParser()

    try:
        result = await bk_parser.start_login(phone)
    except ApiError:
        await message.answer(messages.something_went_wrong_with_api, reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return

    await check_result(result, message, state)

    await state.update_data(phone=phone, login_hash=result['response']['hash'])
    await states.Registration.waiting_for_code.set()
    await message.answer(messages.code_input.format(phone=phone), reply_markup=reply_keyboards.code_input)


async def get_code(message: Message, state: FSMContext):
    code = message.text

    if not code.isdigit() or len(code) != 4:
        await message.answer(messages.bad_code.format(error='Код должен быть из 4 цифр'))
        return

    data = await state.get_data()
    bk_parser = BurgerKingParser()

    try:
        result = await bk_parser.get_token(data['phone'], code, data['login_hash'])
    except ApiError:
        await message.answer(messages.something_went_wrong_with_api, reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return

    await check_result(result, message, state)

    bk_parser.update_token(result['response']['token'])
    user_info = await bk_parser.get_user_info()
    user_check_info = await bk_parser.get_user_check_info()

    db = message.bot.get('database')
    async with db() as session:
        bk_user = await session.get(BKUser, user_info['response']['id'])

        city = await City.get_or_create(session, user_check_info['city'])
        restaurants = list()
        for restaurant in user_check_info['restaurants']:
            restaurants.append(await Restaurant.get_or_create(session, restaurant, city))

        if bk_user:
            bk_user.name = user_check_info['name']
            bk_user.token = result['response']['token']
            bk_user.phone = data['phone']
            bk_user.city = city
            bk_user.restaurants = restaurants
            bk_user.mailing = True
            old_tg_id = bk_user.telegram_id
            bk_user.telegram_id = message.from_id
            await message.bot.send_message(chat_id=old_tg_id, text=messages.unlogin)
        else:
            bk_user = BKUser(
                id=user_info['response']['id'],
                name=user_check_info['name'],
                token=result['response']['token'],
                phone=data['phone'],
                city=city,
                restaurants=restaurants,
                telegram_id=message.from_id
            )
            session.add(bk_user)

        await session.commit()

    await message.answer(messages.hello.format(username=bk_user.name), reply_markup=ReplyKeyboardRemove())
    await state.finish()


def register_registration(dp: Dispatcher):
    dp.register_callback_query_handler(start_registration, text='start_login')

    dp.register_message_handler(new_phone, Text(equals=reply_commands.new_phone_request),
                                state=states.Registration.waiting_for_code)
    dp.register_message_handler(new_code, Text(equals=reply_commands.new_code_request),
                                state=states.Registration.waiting_for_code)

    dp.register_message_handler(get_user_phone, state=states.Registration.waiting_for_phone,
                                content_types=[ContentType.CONTACT, ContentType.TEXT])
    dp.register_message_handler(get_code, state=states.Registration.waiting_for_code)
