from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class Holiday(Base):
    __tablename__ = 'holiday'
    id = Column(Integer, primary_key=True)
    name = Column(String, name='Holiday Name')
    day = Column(String, name='Day')
    month = Column(String, name='Month')
    year = Column(Integer, name='Year')
    datetime = Column(DateTime, name='Holiday Date')



