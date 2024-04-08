# coding: utf-8
from .data_model import DataModel


class Role(DataModel):
    collection = "roles"

    def __init__(self, db, name, permissions=None):
        super().__init__(db, "roles")
        self.name = name
        self.permissions = permissions if permissions else []

    def to_dict(self):
        return {
            "name": self.name,
            "permissions": self.permissions
        }