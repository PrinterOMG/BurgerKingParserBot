from sqlalchemy import Column, BigInteger, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import text

from tgbot.services.database.base import Base


class BKUser(Base):
    __tablename__ = 'bk_user'

    id = Column(Integer, primary_key=True)
    token = Column(String)
    phone = Column(String)

    telegram_id = Column(BigInteger, ForeignKey('telegram_user.telegram_id'))

    telegram_user = relationship('TelegramUser', backref=backref('bk_user', uselist=False))
