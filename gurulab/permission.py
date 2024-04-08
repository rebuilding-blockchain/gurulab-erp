# coding: utf-8
from .data_model import DataModel


class Permission(DataModel):
    collection = "permissions"

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            "name": self.name
        }
