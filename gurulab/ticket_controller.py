# coding: utf-8
from .database_controller import DataBaseController
from .event_controller import EventController
from .ticket import DummyTicket
from datetime import datetime
import uuid


class TicketController(DataBaseController):
    @EventController.event_wrapper(category="ticket", event_type="create")
    def create_ticket(self, ticket_id, ticket_type, ticket_name, source, assign_method='manual', deadline=None):
        ticket_id = str(uuid.uuid4())
        new_ticket = DummyTicket(
            ticket_id=ticket_id,
            ticket_type=ticket_type,
            ticket_name=ticket_name,
            source=source,
            assign_method=assign_method,
            timestamp=datetime.now(),
            deadline=deadline,
            state='open'
        )
        self.db[DummyTicket.collection].insert_one(new_ticket.to_dict())
        return {
            "result": True,
            "event": new_ticket
        }

    @EventController.event_wrapper(category="ticket", event_type="update")
    def update_ticket_state(self, ticket_id, new_state):
        result = self.db[DummyTicket.collection].update_one({"ticket_id": ticket_id}, {"$set": {"state": new_state}})
        return result.modified_count > 0

    @EventController.event_wrapper(category="ticket", event_type="assign")
    def assign(self, ticket, user):



