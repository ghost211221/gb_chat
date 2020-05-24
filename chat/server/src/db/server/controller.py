from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, BigInteger, Boolean, String, ForeignKey, DateTime, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import datetime

""" Контроллер серверной базы данных"""

Base = declarative_base()

class Users(Base):
    """Модель таблицы юзеров"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    userName = Column(String, unique=True)
    userInfo = Column(String)
    userPassHash = Column(String)
    userPubKey = Column(String)
    avatar_id = Column(Integer, ForeignKey('avatars.id'))

    avatars = relationship('Avatars', uselist=True, cascade='delete,all')

    def __init__(self, name, info=None, passHash=None, PubKey=None):
        self.userName = name
        self.userInfo = info
        self.userPassHash = passHash
        self.userPubKey = PubKey

    def __repr__(self):
        return f'<Users({self.userName}, {self.userInfo})>'

class Avatars(Base):
    __tablename__ = 'avatars'
    id = Column(Integer, primary_key=True)
    Data = Column(BLOB)

    def __init__(self, photo):
        self.Data = photo

    def __repr__(self):
        return f'<Avatars({self.id})>'


class UserStories(Base):
    """Модель таблицы истории клиента"""
    __tablename__ = 'userstories'

    id = Column(Integer, primary_key=True)
    UserStoriesUser = Column(Integer, ForeignKey('users.id'))
    userStoriesTime = Column(DateTime)
    userStoriesIP = Column(String)
    userStoriesPort = Column(Integer)

    users = relationship('Users', uselist=True, cascade='delete,all')

    def __init__(self, user_id, datetime, ip, port):
        self.UserStoriesUser = user_id
        self.userStoriesTime = datetime
        self.userStoriesIP = ip
        self.userStoriesPort = port

    def __repr__(self):
        return f'<UserStories({self.userStoriesTime}, {self.userStoriesIP}, \
            {self.userStoriesPort})>'

class Contacts(Base):
    """Модель таблицы контактов"""
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    contactsOwner = Column(Integer, ForeignKey('users.id'))
    contactsClient = Column(Integer, ForeignKey('users.id'))

    owner = relationship("Users", foreign_keys=[contactsOwner])
    client = relationship("Users", foreign_keys=[contactsClient])

    def __init__(self, owner, client):
        self.contactsOwner = owner
        self.contactsClient = client

    def __repr__(self):
        return f'<Contacts({self.contactsOwner}, {self.contactsClient})>'


class Controller():
    """класс контроллера серверного хранилища"""
    def __init__(self):
        self.db_engine = create_engine('sqlite:///server_db.db', \
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

    def new_user(self, username, passhash):
        """добавление нового юзера"""
        user = self.session.query(Users).filter_by(userName=username).first()
        if user:
            return user
        else:
            user = (Users(name=username, passHash=passhash))
            self.session.add(user)
            self.session.commit()
            return user

    def read_users(self):
        """получение списка всех юзеров"""
        users = self.session.query(Users).all()
        return users

    def check_user(self, userName):
        """ проверка наличия пользователя в базе данных """
        return self.session.query(Users).filter_by(userName=userName).first()

    def add_history(self, user_id, ip, port):
        """добавление записи в таблицу истории юзеров"""
        x = (UserStories(user_id=user_id,
                                datetime=datetime.datetime.now(),
                                ip=ip,
                                port=port
                                )
            )
        self.session.add(x)
        self.session.commit()

    def read_history(self, userName):
        user = self.session.query(Users).filter_by(userName=userName).first()
        return self.session.query(UserStories).filter_by(UserStoriesUser=user.id).all()

    ###############################################################################

    def user_login(self, username, ip, port, pubkey):
        """обработка логина"""
        user = self.session.query(Users).filter_by(userName=username).first()
        self.add_history(user.id, ip, port)

    def get_hash(self, name):
        user = self.session.query(Users).filter_by(userName=name).first()
        return user.userPassHash

    def get_pubkey(self , username):
        user = self.session.query(Users).filter_by(userName=username).first()
        return user.userPubKey

    def add_contact(self, owner, client):
        """добавление записей в список контактов юзера"""
        owner_ = self.session.query(Users).filter_by(userName=owner).first()
        client_ = self.session.query(Users).filter_by(userName=client).first()  
        if not owner_:
            return "no owner"
        if not client_:
            return "no client"
        contact = self.session.query(Contacts)\
            .filter_by(contactsOwner=owner_.id)\
            .filter_by(contactsClient=client_.id)\
            .all()
        if contact:
            print(f"contact {owner} -> {client} exists")
        else:
            print(f"contact {owner} -> {client} not exist")
            x = (Contacts(owner=owner_.id, client=client_.id))
            self.session.add(x)
            self.session.commit()
        print("----------------------------------------------")

    def del_contact(self, owner, client):
        """добавление записей в список контактов юзера"""
        owner_ = self.session.query(Users).filter_by(userName=owner).first()
        client_ = self.session.query(Users).filter_by(userName=client).first()  
        self.session.query(Contacts)\
            .filter_by(contactsOwner=owner_.id)\
            .filter_by(contactsClient=client_.id)\
            .delete()
        self.session.commit()

    def read_contacts(self, owner):
        """чтение списка контактов по имени юзера"""
        print(f"reading contacts of {owner}")
        owner_ = self.session.query(Users).filter_by(userName=owner).first()
        print(owner_)
        contacts = self.session.query(Users).outerjoin(Contacts, Contacts.contactsClient==Users.id).filter_by(contactsOwner=owner_.id).all()

        return self.__genDict(contacts)

    def add_avatar(self, owner, photo):
        print('adding avatar')
        owner_ = self.session.query(Users).filter_by(userName=owner).first()
        print(owner_)

        avatar = Avatars(photo=photo)
        print(avatar)
        self.session.add(avatar)
        self.session.commit()
        print(avatar)
        owner_.avatar_id = avatar.id
        self.session.commit()     

    def get_avatar(self, owner):
        print("get avatat from db")
        print(owner)
        owner_ = self.session.query(Users).filter_by(userName=owner).first()

        avatar = self.session.query(Avatars).filter_by(id=owner_.avatar_id).order_by(Avatars.id.desc()).first() # эт ж новый аватар
          
        return avatar.Data if avatar else bytearray()

if __name__ == '__main__':
    test_db = Controller()
    # выполняем 'подключение' пользователя
    test_db.user_login('client_1', '192.168.1.4', 8888)
    test_db.user_login('client_2', '192.168.1.5', 7777)
    test_db.user_login('client_3', '192.168.1.5', 6666)
    test_db.user_login('client_4', '192.168.1.5', 5555)

    test_db.add_contact('client_1', 'client_2')
    test_db.add_contact('client_1', 'client_3')
    test_db.add_contact('client_1', 'client_4')

    test_db.add_contact('client_2', 'client_3')

    test_db.add_contact('client_3', 'client_1')

    print(test_db.read_contacts('client_1'))

    test_db.del_contact('client_1', 'client_4')

    print(test_db.read_contacts('client_1'))