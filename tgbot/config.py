from dataclasses import dataclass

from environs import Env


@dataclass
class TelegramBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    bk_token: str


@dataclass
class Config:
    bot: TelegramBot
    misc: Miscellaneous


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
            bk_token=env.str('BURGER_KING_TOKEN')
        )
    )
