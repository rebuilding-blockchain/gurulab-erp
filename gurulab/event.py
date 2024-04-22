# coding: utf-8
from .data_model import DataModel


class Event(DataModel):
    collection = "event"

    def __init__(self, category, event_type, data=None):
        self.category = category
        self.event_type = event_type
        self.data = data

    def to_dict(self):
        return {
            "category": self.category,
            "event_type": self.event_type,
            "data": self.data
        }

    @classmethod
    def from_dict(cls, data):
        return Event(category=data["category"], event_type=data["event_type"], data=data["data"])
