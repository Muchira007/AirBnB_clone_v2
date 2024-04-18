#!/usr/bin/python3
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base, BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """
    This class manages database storage with SQLAlchemy.
    """

    __engine = None
    __session = None

    def __init__(self):
        """ Initializes DBStorage instance. """
        try:
            user = os.getenv("HBNB_MYSQL_USER")
            pwd = os.getenv("HBNB_MYSQL_PWD")
            host = os.getenv("HBNB_MYSQL_HOST", "localhost")
            db = os.getenv("HBNB_MYSQL_DB")
            self.__engine = create_engine(
                    f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
                    pool_pre_ping=True)
            if os.getenv("HBNB_ENV") == "test":
                Base.metadata.drop_all(self.__engine)
            Session = scoped_session(sessionmaker(
                bind=self.__engine, expire_on_commit=False))
            self.__session = Session()
        except Exception as e:
            print(f"Error initializing DBStorage: {e}")

    def all(self, cls=None):
        """ Query all objects from the current database session. """
        try:
            # If cls is a string, resolve the class using globals()
            if isinstance(cls, str):
                cls = globals().get(cls)

            # If cls is None, query all subclasses of Base
            if cls is None:
                classes = Base.__subclasses__()
            else:
                classes = [cls]

            objects = {}
            for cls in classes:
                query = self.__session.query(cls)
                for obj in query:
                    key = f"{cls.__name__}.{obj.id}"
                    objects[key] = obj
            return objects
        except Exception as e:
            print(f"Error in all method: {e}")
            return {}

    def new(self, obj):
        """ Add the object to the current database session. """
        try:
            if obj:
                self.__session.add(obj)
        except Exception as e:
            print(f"Error adding object to session: {e}")

    def save(self):
        """ Commit all changes of the current database session. """
        try:
            self.__session.commit()
        except Exception as e:
            print(f"Error saving session: {e}")

    def delete(self, obj=None):
        """ Delete obj from the current database session. """
        try:
            if obj:
                self.__session.delete(obj)
        except Exception as e:
            print(f"Error deleting object from session: {e}")

    def reload(self):
        """ Create all tables and initialize session from the engine. """
        try:
            Base.metadata.create_all(self.__engine)
        except Exception as e:
            print(f"Error creating tables: {e}")

        try:
            self.__session.close()
            Session = scoped_session(sessionmaker(
                bind=self.__engine, expire_on_commit=False))
            self.__session = Session()
        except Exception as e:
            print(f"Error reloading session: {e}")
