#!/usr/bin/env python3
"""db
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB
    """

    def __init__(self):
        """init
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """_session
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add_user
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """find_user_by
        """
        user_keys = ['id', 'email', 'hashed_password', 'session_id',
                     'reset_token']
        for key in kwargs.keys():
            if key not in user_keys:
                raise InvalidRequestError
        result = self._session.query(User).filter_by(**kwargs).first()
        if result is None:
            raise NoResultFound
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """update_user
        """
        user_to_update = self.find_user_by(id=user_id)
        user_keys = ['id', 'email', 'hashed_password', 'session_id',
                     'reset_token']
        for key, value in kwargs.items():
            if key in user_keys:
                setattr(user_to_update, key, value)
            else:
                raise ValueError
        self._session.commit()
