from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import datetime

Base = declarative_base()

class Story(Base):
    """Модель таблицы истории сообщений клиента"""
    __tablename__ = 'story'

    id = Column(Integer, primary_key=True)
    StorySend = Column(String)
    StoryDest = Column(String) 
    StoryTime = Column(DateTime)
    StoryMessage = Column(String)


    def __init__(self, sender, destination, datetime, message):
        self.StorySend = sender
        self.StoryDest = destination
        self.StoryTime = datetime
        self.StoryMessage = message

    def __repr__(self):
        return f'<Story({self.StoryTime}, {self.StoryDest}, {self.StoryMessage})>'

class Contacts(Base):
    """Модель таблицы контактов"""
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    contactsOwner = Column(String)
    contactsClient = Column(String)

    def __init__(self, owner, client):
        self.contactsOwner = owner
        self.contactsClient = client

    def __repr__(self):
        return f'<Contacts({self.contactsOwner}, {self.contactsClient})>'


class Controller():
    """класс контроллера серверного хранилища"""
    def __init__(self):
        self.db_engine = create_engine('sqlite:///client_db.db', \
            echo=False, pool_recycle=3600)
        Base.metadata.create_all(self.db_engine)

        Session = sessionmaker(bind=self.db_engine)
        self.session = Session()

    def __genDict(self, query):
        retDictList = []
        for item in query:
            tempDict = {}
            for field in [x for x in dir(item) if not x.startswith('_') and x != 'metadata']:
                tempDict.update(
                    {
                        field: item.__getattribute__(field)
                    }
                )
            retDictList.append(tempDict)
        return retDictList

    def add_history(self, sender, destination, message):
        """добавление записи в таблицу истории юзеров"""
        x = (Story( sender=sender,
                    destination=destination,
                    datetime=datetime.datetime.now(),
                    message=message
                )
            )
        self.session.add(x)
        self.session.commit()

    def read_history(self, user, dest):
        """чтение истории чата"""
        story = self.session.query(Story).filter_by(StorySend=user).filter_by(StoryDest=dest).all()
        return story

    ###############################################################################
    def add_contact(self, owner, client):
        """добавление записей в список контактов юзера"""
        contact = self.session.query(Contacts)\
            .filter_by(contactsOwner=owner)\
            .filter_by(contactsClient=client)\
            .all()
        if contact:
            print(f"contact {owner} -> {client} exists")
        else:
            print(f"contact {owner} -> {client} not exist")
            x = (Contacts(owner=owner, client=client))
            self.session.add(x)
            self.session.commit()
        print("----------------------------------------------")

    def del_contact(self, owner, client):
        """удаление записей из списка контактов юзера"""
        self.session.query(Contacts)\
            .filter_by(contactsOwner=owner)\
            .filter_by(contactsClient=client)\
            .delete()
        self.session.commit()

    def read_contacts(self, owner):
        """чтение списка контактов по имени юзера"""
        print(f"reading contacts of {owner}")
        print(owner_)
        contacts = self.session.query(Contacts).filter_by(contactsOwner=owner).all()

        return self.__genDict(contacts)


if __name__ == '__main__':
    test_db = Controller()

    test_db.add_history("guest0", "guest1", datetime.datetime.now(), "hello")
    test_db.add_history("guest0", "guest2", datetime.datetime.now(), "hello")
    test_db.add_history("guest0", "guest3", datetime.datetime.now(), "hello")
    test_db.add_history("guest0", "guest4", datetime.datetime.now(), "hello")

    """ вывод через sqlite manager в firefox:
        id  StorySend   StoryDest   StoryTime   StoryMessage
1   1   guest0  guest1  2020-02-21 05:17:28.598387  hello
2   2   guest0  guest2  2020-02-21 05:17:28.682487  hello
3   3   guest0  guest3  2020-02-21 05:17:28.767433  hello
4   4   guest0  guest4  2020-02-21 05:17:28.852887  hello
    """