from sqlalchemy import Column, BigInteger, DateTime, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import text

from tgbot.services.database.base import Base


user_restaurants = Table(
    'user_restaurant',
    Base.metadata,
    Column('bk_user_id', BigInteger, ForeignKey('bk_user.id'), primary_key=True),
    Column('restaurant_id', Integer, ForeignKey('restaurant.id'), primary_key=True)
)


class BKUser(Base):
    __tablename__ = 'bk_user'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    token = Column(String)
    phone = Column(String)

    mailing = Column(Boolean, default=True)

    city_id = Column(Integer, ForeignKey('city.id'))
    telegram_id = Column(BigInteger, ForeignKey('telegram_user.telegram_id'))

    city = relationship('City')
    restaurants = relationship('Restaurant', secondary=user_restaurants)
    telegram_user = relationship('TelegramUser', backref=backref('bk_user', uselist=False))
