# coding: utf-8
from .database_controller import DataBaseController
from datetime import datetime
import uuid
from .ticket_template import TicketTemplate
from typing import Dict, List, Optional
from .ticket_template import StateTransition, SubTicketCreationTrigger
from pymongo.errors import DuplicateKeyError


class TicketController(DataBaseController):
    @classmethod
    def get_ticket_template_by_name(cls, name: str) -> TicketTemplate:
        """
        根据工单模板的名称获取一个工单模板。
        """
        # 注意这里使用了 'ticket_templates' 集合
        template_data = cls.db[TicketTemplate.collection].find_one({"name": name})
        if template_data:
            ticket_template = TicketTemplate.from_dict(template_data)
        else:
            ticket_template = None
        return ticket_template

    @classmethod
    def get_ticket_template_by_id(cls, ticket_template_id: str) -> TicketTemplate:
        """
        根据工单模板的id获取一个工单模板。
        """
        # 注意这里使用了 'ticket_templates' 集合
        template_data = cls.db[TicketTemplate.collection].find_one({"template_id": ticket_template_id})
        if template_data:
            ticket_template = TicketTemplate.from_dict(template_data)
        else:
            ticket_template = None
        return ticket_template

    @classmethod
    def get_all_ticket_templates(cls) -> List[TicketTemplate]:
        """
        获取所有工单模板。
        """
        # 同样，这里使用了 'ticket_templates' 集合
        templates = cls.db[TicketTemplate.collection].find({})
        ticket_templates = [TicketTemplate.from_dict(template) for template in templates]
        return ticket_templates

    @classmethod
    def create_ticket_template(
            cls,
            name: str,
            initial_state: str,
            state_transitions: Dict[str, Dict[str, StateTransition]] = None,
            sub_ticket_creation_triggers: Dict[str, List[SubTicketCreationTrigger]] = None,
            sub_ticket_transitions: Optional[Dict[str, List[str]]] = None
    ) -> Optional[str]:
        # 检查数据库中是否已存在具有相同名称的模板
        existing_template = cls.db[TicketTemplate.collection].find_one({"name": name})
        if existing_template:
            print(f"A ticket template with the name '{name}' already exists.")
            return None  # 或者返回已存在模板的ID：return existing_template["template_id"]

        # 如果名称唯一，则创建新模板
        try:
            template_id = str(uuid.uuid4())  # 生成唯一的模板ID
            new_template = TicketTemplate(
                template_id=template_id,
                name=name,
                initial_state=initial_state,
                state_transitions=state_transitions,
                sub_ticket_creation_triggers=sub_ticket_creation_triggers,
                sub_ticket_transitions=sub_ticket_transitions
            )
            cls.db[TicketTemplate.collection].insert_one(new_template.to_dict())
            return template_id
        except DuplicateKeyError:
            print("A ticket template with the same template_id already exists.")
            return None

    @classmethod
    def delete_ticket_template(cls, template_id: str) -> bool:
        """
        根据工单模板的ID删除一个工单模板。

        :param template_id: 要删除的工单模板的ID。
        :return: 删除操作是否成功完成。
        """
        # 查询数据库以确保模板存在
        existing_template = cls.db[TicketTemplate.collection].find_one({"template_id": template_id})
        if not existing_template:
            print(f"No ticket template found with ID '{template_id}'.")
            return False

        # 执行删除操作
        result = cls.db[TicketTemplate.collection].delete_one({"template_id": template_id})

        # 根据删除操作的结果返回成功或失败
        if result.deleted_count > 0:
            print(f"Ticket template with ID '{template_id}' was successfully deleted.")
            return True
        else:
            print(f"Failed to delete ticket template with ID '{template_id}'.")
            return False
