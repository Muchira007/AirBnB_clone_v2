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
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST", "localhost")
        db = os.getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(
                f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
                pool_pre_ping=True)
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query all objects from the current database session. """
        # If cls is a string, resolve the class using globals()
        if isinstance(cls, str):
            try:
                cls = globals()[cls]
            except KeyError:
                pass

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

    def new(self, obj):
        """ Add the object to the current database session. """
        if obj:
            self.__session.add(obj)
            self.__session.commit()

    def save(self):
        """ Commit all changes of the current database session. """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete obj from the current database session. """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables and initialize session from the engine. """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
