from .data_model import DataModel
from typing import TypedDict, List


class Component(TypedDict):
    element_template_id: str
    quantity: int


class ElementTemplate(DataModel):
    collection = "element_templates"

    def __init__(self, template_id, name, category="dummy", component_templates: List[Component] = None):
        """

        :param name:
        :param category: category "dummy" is the very basic element which has no component_templates.
        :param component_templates: [{ElementTemplateInstance.name: quantity}, {ElementTemplateInstance.name: quantity}]
        """
        self.template_id = template_id
        self.name = name
        self.category = category
        # component_templates存储结构为字典，键为组件名称，值为数量
        self.component_templates = component_templates if component_templates is not None else []

    def to_dict(self):
        """
        将ElementTemplate对象序列化为字典。
        """
        return {
            "template_id": self.template_id,
            "name": self.name,
            "category": self.category,
            "component_templates": self.component_templates
        }

    @classmethod
    def from_dict(cls, data):
        """
        从字典反序列化为ElementTemplate对象。
        """
        return cls(
            template_id=data.get("template_id"),
            name=data.get("name"),
            category=data.get("category", "dummy"),
            component_templates=data.get("component_templates", [])
        )

    def __repr__(self):
        return f"ElementTemplate(name={self.name}, component_templates={self.component_templates})"

    def add_component_template(self, component_template, quantity):
        # No validity check here, do it in controller
        self.component_templates[component_template.name] = quantity

    def remove_component_template(self, component_template):
        # 删除组件模板，如果组件不存在则忽略
        self.component_templates.pop(component_template.name)
