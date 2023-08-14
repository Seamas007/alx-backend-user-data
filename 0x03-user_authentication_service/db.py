#!/usr/bin/env python3
"""
Database nodule
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """ Model Data Base """

    def __init__(self):
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """ Make sessions """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()

        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
            Make a new user

            Args:
                email: Text email
                hashed_password: Password hashed

            Return:
                User created
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
            Find user based in composition of your features

            Args:
                kwargs: Arbitrary dict with features

            Return:
                User found or error name
        """
        if not kwargs:
            raise InvalidRequestError

        cols_keys = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in cols_keys:
                raise InvalidRequestError

        users = self._session.query(User).filter_by(**kwargs).first()

        if users is None:
            raise NoResultFound

        return users

    def update_user(self, user_id: int, **kwargs) -> None:
        """
            Update user in the database

            Args:
                user_id: Id to find and modify user
                kwargs: Arbitrary dict with features

            Return:
                None
        """
        if not kwargs:
            return None

        user = self.find_user_by(id=user_id)

        cols_keys = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in cols_keys:
                raise ValueError

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
