# coding: utf-8
from .data_model import DataModel


class Element(DataModel):
    collection = "elements"

    def __init__(self, name, template=None, components=None):
        """
        初始化Element实例。

        :param name: 元素的名称。
        :param template: ElementTemplate实例，定义此Element的类型和结构。
        :param components: 组成此Element的子Element列表。
        """
        self.name = name
        self.template = template  # ElementTemplate实例
        self.components = components if components is not None else []

    def add_component(self, component):
        """
        向此Element添加一个子Element。

        :param component: 要添加的子Element。
        """
        if self.template and component.name in self.template.component_templates:
            self.components.append(component)
        else:
            print(f"Warning: Adding a component that is not defined in the template for {self.name}.")

    def to_dict(self):
        """
        实现DataModel的to_dict方法，以便Element实例能够序列化。
        """
        return {
            "name": self.name,
            "template": self.template.name if self.template else None,
            "components": [component.to_dict() for component in self.components]
        }

    @classmethod
    def from_dict(cls, data_dict):
        """
        从字典创建Element实例的类方法。

        :param data_dict: 包含Element属性的字典。
        :return: Element实例。
        """
        name = data_dict.get("name")
        template_name = data_dict.get("template")
        component_dicts = data_dict.get("components", [])

        # 假设已有方法从名称加载ElementTemplate实例
        template = ElementTemplate.load(template_name) if template_name else None

        components = [cls.from_dict(comp_dict) for comp_dict in component_dicts]

        return cls(name, template, components)

    def __repr__(self):
        return f"Element(name={self.name}, template={self.template}, components={self.components})"
