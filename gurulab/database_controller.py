# coding: utf-8
from .config import db_name
from pymongo import MongoClient


class DataBaseController:
    db_client = MongoClient('mongodb://localhost:27017/')
    db = db_client[db_name]
