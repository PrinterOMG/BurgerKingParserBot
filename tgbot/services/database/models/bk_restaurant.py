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

    @classmethod
    async def get_or_create(cls, session, api_restaurant, city):
        restaurant = await session.get(Restaurant, api_restaurant['id'])

        if restaurant is None:
            restaurant = Restaurant(id=api_restaurant['id'], address=api_restaurant['address'], city=city)
            session.add(restaurant)
            await session.commit()

        return restaurant
