from sqlalchemy import Column, BigInteger, DateTime, Integer, String
from sqlalchemy.sql.expression import text

from tgbot.services.database.base import Base


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    @classmethod
    async def get_or_create(cls, session, api_city: dict):
        city = await session.get(City, api_city['id'])
        if city is None:
            city = City(id=api_city['id'], name=api_city['name'])
            session.add(city)
            await session.commit()

        return city
