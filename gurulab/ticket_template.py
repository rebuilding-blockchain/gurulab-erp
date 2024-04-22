from typing import Dict, List, TypedDict, Optional
from .data_model import DataModel
from .element_template import ElementTemplate


# 重新定义sub_ticket_creation_triggers为字典，以action为key
class SubTicketCreationTrigger(TypedDict):
    sub_template_id: str
    initial_state: str


class StateTransition(TypedDict):
    action: str
    description: Optional[str]  # 可选字段，用于描述这个状态转换


class SubTicketTrigger(TypedDict):
    action: str
    next_state: str
    sub_template_id: str


class TicketTemplate(DataModel):
    """
    Every ticket is related to "something".  A ticket assigns something to somebody.
    A Ticket Template defines how to deal with "something".
    """
    collection = "ticket_templates"

    def __init__(
            self,
            template_id: str,
            name: str,
            initial_state: str,
            state_transitions: Dict[str, Dict[str, StateTransition]] = None,
            sub_ticket_creation_triggers: Dict[str, List[SubTicketCreationTrigger]] = None,
            sub_ticket_transitions: Dict[str, List[StateTransition]] = None,
            element_templates:List[ElementTemplate] = None
    ):
        """
        初始化TicketTemplate实例。

        :param template_id: TicketTemplate的唯一标识符。
        :param name: TicketTemplate的名称。
        :param initial_state: Ticket的初始状态。
        :param state_transitions: 描述状态转移的字典，键是状态，值是StateTransition类型的列表。
        :param sub_ticket_creation_triggers: 定义在特定动作和状态下触发子工单创建的规则。
        """
        if sub_ticket_creation_triggers is None:
            sub_ticket_creation_triggers = dict()
        if sub_ticket_transitions is None:
            sub_ticket_transitions = dict()
        self.template_id = template_id
        self.name = name
        self.initial_state = initial_state
        self.state_transitions = state_transitions
        self.sub_ticket_creation_triggers = sub_ticket_creation_triggers
        self.sub_ticket_transitions = sub_ticket_transitions
        self.element_templates = element_templates

    def add_element_template(self, element_template) -> bool:
        if element_template not in self.element_templates:
            self.element_templates.append(element_template)
            return True
        else:
            return False

    def del_element_template(self, element_template) -> bool:
        if element_template in self.element_templates:
            self.element_templates.pop(element_template)
            return True
        else:
            return False

    def to_dict(self):
        """
        将TicketTemplate对象序列化为字典。
        """
        return {
            "template_id": self.template_id,
            "name": self.name,
            "initial_state": self.initial_state,
            "state_transitions": self.state_transitions,
            "sub_ticket_creation_triggers": self.sub_ticket_creation_triggers,
            "sub_ticket_transitions": self.sub_ticket_transitions
        }

    @classmethod
    def from_dict(cls, data):
        """
        从字典反序列化为TicketTemplate对象。
        """
        return cls(
            template_id=data["template_id"],
            name=data["name"],
            initial_state=data["initial_state"],
            state_transitions=data["state_transitions"],
            sub_ticket_creation_triggers=data.get("sub_ticket_triggers", [])
        )

    def __repr__(self) -> str:
        return f"TicketTemplate(template_id='{self.template_id}', name='{self.name}')"