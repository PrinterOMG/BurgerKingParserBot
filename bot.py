import asyncio
import datetime
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aioredis import Redis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from tgbot.config import load_config
from tgbot import handlers
from tgbot import filters
from tgbot import middlewares
from tgbot.services.bk_parser.parser import BurgerKingParser
from tgbot.services.database.base import Base
from tgbot.services.schedulers import start_schedulers, send_dates

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(middlewares.EnvironmentMiddleware(config=config))
    dp.setup_middleware(middlewares.ThrottlingMiddleware())


def register_all_filters(dp):
    for aiogram_filter in filters.filters:
        dp.filters_factory.bind(aiogram_filter)


def register_all_handlers(dp):
    for register in handlers.register_functions:
        register(dp)


async def main():
    log_file = rf'logs/{datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.log'
    if not os.path.exists('logs'): os.mkdir('logs')
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        handlers=(logging.FileHandler(log_file), logging.StreamHandler())
    )
    logger.info('Starting bot')
    config = load_config('.env')

    bot = Bot(token=config.bot.token, parse_mode='HTML')
    bot_info = await bot.me
    logger.info(f'Bot: {bot_info.username} [{bot_info.mention}]')

    storage = RedisStorage2(host='redis') if config.bot.use_redis else MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    redis = Redis(host='redis')

    engine = create_async_engine(
        f'postgresql+asyncpg://{config.database.user}:{config.database.password}@postgres/{config.database.name}',
        future=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_sessionmaker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession, future=True)

    bot['config'] = config
    bot['redis'] = redis
    bot['database'] = async_sessionmaker

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    asyncio.create_task(start_schedulers(bot, async_sessionmaker))

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()

        bot_session = await bot.get_session()
        await bot_session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit) as e:
        logger.error('Bot stopped!')
        raise e
