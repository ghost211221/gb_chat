from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, BigInteger, Boolean, String, ForeignKey, DateTime, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from aiopg.sa import create_engine as aio_ce

import asyncio

import datetime

from databases import Database
database = Database('sqlite:///example.db')

""" Контроллер серверной базы данных"""

Base = declarative_base()

class Texts(Base):
    """Модель таблицы юзеров"""
    __tablename__ = 'texts'

    id = Column(Integer, primary_key=True)
    text = Column(String)

    def __init__(self, text):
        self.text = text
    def __repr__(self):
        return f'<Users({self.text}>'


if __name__ == "__main__":

    db_engine = create_engine('sqlite:///test.db', echo=False, pool_recycle=3600)
    Base.metadata.create_all(db_engine)

    Session = sessionmaker(bind=db_engine)
    session = Session()

    lines = [
        'Выполняем задачи с использованием базы данных.',
        'Написать программу для поиска заданной строки в тексте.',
        'Сделать чат для всех пользователей.',
        'Реализовать поиск по контактам.',
        '* Сделать асинхронными все запросы к базе данных',
        '* Сделать сохранение результатов поиска',
        '* Сделать асинхронный поиск строки в тексте',
    ]

    for line in lines:
        text = Texts(text=line)
        session.add(text)

    session.commit()

    q = session.query(Texts.text).filter(Texts.text.ilike("%все%"))

    records = q.all()

    for row in records:
        print(row.text)