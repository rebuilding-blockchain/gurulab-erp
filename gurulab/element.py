# coding: utf-8
from .data_model import DataModel
from typing import List, Dict, Any, TypedDict


class ElementComponent(TypedDict):
    component_template_name: str
    quantity: int
    component_elements: List[str]


class Element(DataModel):
    collection = "elements"

    def __init__(
            self, element_id: str, template_id: str, properties: Dict[str, Any] = None, 
            position: int = None, components: Dict[str, ElementComponent] = None, component_of: str = None):
        """
        初始化一个Element实例。
        :param element_id: Element的唯一标识符。
        :param template_id: 与此Element相关联的ElementTemplate的唯一标识符。
        :param properties: 包含Element的特定属性和值的字典。
        :param position: Element作为组件时的位置信息。
        :param components: 与此Element相关的组件实例字典。
        :param component_of: 此Element作为组件属于的父Element的element_id。
        """
        self.element_id = element_id
        self.template_id = template_id
        self.properties = properties if properties is not None else {}
        self.position = position
        self.components = components if components is not None else {}
        self.component_of = component_of

    def to_dict(self):
        """
        将Element对象序列化为字典。
        """
        return {
            "element_id": self.element_id,
            "template_id": self.template_id,
            "properties": self.properties,
            "position": self.position,
            "components": self.components,
            "component_of": self.component_of
        }

    @classmethod
    def from_dict(cls, data):
        """
        从字典反序列化为Element对象。
        """
        return cls(
            element_id=data["element_id"],
            template_id=data["template_id"],
            properties=data.get("properties", {}),
            position=data.get("position"),
            components=data.get("components", {}),
            component_of=data.get("component_of")
        )

    def __repr__(self):
        components_repr = {key: {"quantity": value["quantity"], "component_elements": value["component_elements"]} for key, value in self.components.items()}
        return (f"Element(element_id='{self.element_id}', template_id='{self.template_id}', "
                f"properties={self.properties}, position={self.position}, "
                f"components={components_repr})")
