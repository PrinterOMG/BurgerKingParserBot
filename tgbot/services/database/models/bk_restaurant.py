from sqlalchemy import Column, BigInteger, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from tgbot.services.database.base import Base


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)

    bk_city_id = Column(Integer, ForeignKey('city.id'))

    city = relationship('City', backref='restaurant')
