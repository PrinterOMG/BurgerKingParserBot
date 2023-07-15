from sqlalchemy import Column, BigInteger, DateTime, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from tgbot.services.database.base import Base


class SavedDate(Base):
    __tablename__ = 'saved_date'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)

    bk_user_id = Column(Integer, ForeignKey('bk_user.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

    bk_user = relationship('BKUser', backref='saved_dates')
    restaurant = relationship('Restaurant')
