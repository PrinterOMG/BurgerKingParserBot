from sqlalchemy import Column, BigInteger, DateTime, Integer, String
from sqlalchemy.sql.expression import text

from tgbot.services.database.base import Base


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
