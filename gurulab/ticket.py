from abc import ABC, abstractmethod
from datetime import datetime
import json
from typing import List, Optional, Dict, Union
from .user import User
from .data_model import DataModel


class Ticket(ABC, DataModel):
    """
    A ticket connects something and someone.
    something is wrong -> a ticket indicates this -> assign to someone/some group.
    """
    collection = "tickets"

    def __init__(
            self,
            ticket_type: str,
            ticket_id: str,
            ticket_name: str,
            source: int,
            head_ticket: Optional['Ticket'] = None,
            upstream_ticket: Optional['Ticket'] = None,
            assign_method='manual', # manual, auto
            assigned_by: Optional['User'] = None,
            assigned_to: Optional['User'] = None,
            timestamp=datetime.now(),
            deadline=None,
            state='open'
    ):
        self.ticket_type = ticket_type
        self.ticket_id = ticket_id
        self.ticket_name = ticket_name
        self.source = source
        self.upstream_ticket = upstream_ticket
        self.assign_method = assign_method
        self.assigned_by = assigned_by
        self.assigned_to = assigned_to
        self.timestamp = timestamp
        self.deadline = deadline
        self.state = state
        self.sub_tickets = []
        self.next_tickets = []

    @abstractmethod
    def sub_tickets(self):
        """
        Return a list of sub-tickets which should be automatically generated
        simultaneously with the ticket.
        """
        pass

    @abstractmethod
    def next(self):
        """
        Return a list of tickets which should be generated after this
        ticket is closed or finished.
        """
        pass

    @abstractmethod
    def auto_assign(self):
        """
        if auto_assign returns None, it should be manually assigned.
        :return: User
        """
        return None

    def to_dict(self):
        """
        Serialize the ticket to a dict for MongoDB storage.
        """
        return {
            "ticket_id": self.ticket_id,
            "ticket_type": self.ticket_type,
            "ticket_name": self.ticket_name,
            "source": self.source,
            "upstream_ticket": self.upstream_ticket,
            "assign_method": self.assign_method,
            "assigned_by": self.assigned_by.username if self.assigned_by is not None else None,
            "assigned_to": self.assigned_to.username if self.assigned_to is not None else None,
            "timestamp": self.timestamp.isoformat(),
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "state": self.state
        }


# Example of a concrete implementation of Ticket, which is like a single item of a todo-list
class DummyTicket(Ticket):
    def __init__(self, *args, **kwargs):
        kwargs["ticket_type"] = "DummyTicket"
        super(DummyTicket, self).__init__(*args, **kwargs)

    def sub_tickets(self):
        # 示例: 返回一个空列表，表示没有子工单
        return []

    def next(self):
        # 示例: 返回一个空列表，表示没有后续工单
        return []

    def auto_assign(self):
        # 示例: 返回None，表示需要手动分配
        return None


class ElectronicMaintenanceTicket(Ticket):
    def __init__(self, *args, **kwargs):
        kwargs["ticket_type"] = "ElectronicMaintenance"
