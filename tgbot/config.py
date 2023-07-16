from dataclasses import dataclass

from environs import Env


@dataclass
class Database:
    user: str
    password: str
    name: str


@dataclass
class TelegramBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    pass


@dataclass
class Config:
    bot: TelegramBot
    misc: Miscellaneous
    database: Database


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        bot=TelegramBot(
            token=env.str('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMINS'))),
            use_redis=env.bool('USE_REDIS'),
        ),
        misc=Miscellaneous(

        ),
        database=Database(
            name=env.str('POSTGRES_DB'),
            user=env.str('POSTGRES_USER'),
            password=env.str('POSTGRES_PASSWORD')
        )
    )
