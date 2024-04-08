from abc import ABC, abstractmethod
from pymongo import MongoClient
from .config import db_name


class DataModel(ABC):
    db = db_name

    @abstractmethod
    def to_dict(self):
        """
        Every data model should implement to_dict method to make it serializable
        :return: dict
        """
        pass

    @abstractmethod
    def from_dict(cls, data):
        """
        :return: instance of DataModel subclass
        """
        pass
