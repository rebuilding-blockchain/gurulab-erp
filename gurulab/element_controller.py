# coding:utf-8
from .database_controller import DataBaseController
from .element_template import ElementTemplate
from .element import Element
import uuid


class ElementController(DataBaseController):

    @classmethod
    def get_template_by_name(cls, name):
        template_data = cls.db.templates.find_one({"name": name})
        if not template_data:
            print(f"Template '{name}' not found.")
            return None
        return ElementTemplate.from_dict(template_data)

    @classmethod
    def get_template_by_id(cls, template_id):
        template_data = cls.db.templates.find_one({"template_id": template_id})
        if not template_data:
            print(f"Template '{template_id}' not found.")
            return None
        return ElementTemplate.from_dict(template_data)

    @classmethod
    def get_template_id_by_name(cls, template_name):
        template_data = cls.db.templates.find_one({"name": template_name})
        if template_data:
            return template_data.get("template_id")
        else:
            print(f"Template '{template_name}' not found.")
            return None

    @classmethod
    def new_element_template(cls, name, category="dummy", component_templates=None):
        if not cls.get_template_by_name(name=name):
            template_id = str(uuid.uuid4())  # 生成唯一的template_id
            element_template = ElementTemplate(template_id=template_id, name=name, category=category, component_templates=component_templates)
            res = cls.db.templates.insert_one(element_template.to_dict())
            print(f"New template added with ID: {res.inserted_id}")
            return True
        else:
            print(f"Template '{name}' already exists.")
            return False

    @classmethod
    def add_component_templates(cls, element_template_name, component_template_name, quantity):
        # 通过element_template_name获取目标ElementTemplate的ID
        element_template_data = cls.db.templates.find_one({"name": element_template_name})
        if not element_template_data:
            print(f"Element template with name '{element_template_name}' not found.")
            return False
        element_template_id = element_template_data['template_id']

        # 通过component_template_name获取ComponentTemplate的ID以确认其存在
        component_template_data = cls.db.templates.find_one({"name": component_template_name})
        if not component_template_data:
            print(f"Component template with name '{component_template_name}' not found.")
            return False
        component_template_id = component_template_data['template_id']

        # 检查ComponentTemplate是否已经存在于ElementTemplate的components中
        existing_components = element_template_data.get('component_templates', [])
        for component in existing_components:
            if component['element_template_id'] == component_template_id:
                print(
                    f"Component template '{component_template_name}' is already a part of element template '{element_template_name}'.")
                return False

        # 添加新的component template
        new_component = {"element_template_id": component_template_id, "quantity": quantity}
        updated_components = existing_components + [new_component]
        cls.db.templates.update_one({"template_id": element_template_id},
                                    {"$set": {"component_templates": updated_components}})
        print(f"Added component template '{component_template_name}' to element template '{element_template_name}'.")
        return True

    @classmethod
    def get_all_templates(cls):
        templates = cls.db.templates.find()
        return [ElementTemplate.from_dict(template) for template in templates]

    @classmethod
    def delete_component_templates(cls, element_template_name, component_template_name):
        template = cls.get_template_by_name(name=element_template_name)
        if not template:
            print(f"Template '{element_template_name}' not found.")
            return False

        # 找到并删除指定的组件模板
        original_length = len(template.component_templates)
        template.component_templates = [comp for comp in template.component_templates if
                                        comp["element_template_name"] != component_template_name]

        if len(template.component_templates) < original_length:
            # 更新数据库记录
            update_result = cls.db.templates.update_one(
                {"name": element_template_name},
                {"$set": {"component_templates": template.component_templates}}
            )

            if update_result.modified_count > 0:
                print(f"Component template '{component_template_name}' removed from '{element_template_name}'.")
                return True
            else:
                print("Failed to update the template.")
                return False
        else:
            print(f"Component template '{component_template_name}' not found in '{element_template_name}'.")
            return False

    @classmethod
    def delete_element_template(cls, name):
        # 首先，检查是否有其他模板使用了这个模板作为组件
        all_templates = cls.db.templates.find()
        for template_data in all_templates:
            template = ElementTemplate.from_dict(template_data)
            for component in template.component_templates:
                if component["element_template_name"] == name:
                    print(f"Cannot delete template '{name}' because it is used as a component in '{template.name}'.")
                    return False

        # 如果没有其他模板使用这个模板作为组件，则进行删除操作
        delete_result = cls.db.templates.delete_one({"name": name})
        if delete_result.deleted_count > 0:
            print(f"Template '{name}' deleted.")
            return True
        else:
            print(f"Template '{name}' not found.")
            return False

    @classmethod
    def change_template_name(cls, old_name, new_name):
        # 检查新名称是否已经存在
        if cls.db.templates.find_one({"name": new_name}):
            print(f"Template name '{new_name}' is already in use.")
            return False

        # 根据旧名称找到并更新模板名称
        update_result = cls.db.templates.update_one(
            {"name": old_name},
            {"$set": {"name": new_name}}
        )

        if update_result.modified_count > 0:
            print(f"Template name changed from '{old_name}' to '{new_name}'.")
            return True
        else:
            print(f"Template with name '{old_name}' not found.")
            return False

    @classmethod
    def change_template_category(cls, template_name, new_category):
        # 获取模板
        template_data = cls.db.templates.find_one({"name": template_name})
        if not template_data:
            print(f"Template with name '{template_name}' not found.")
            return False

        # 检查components是否为空，以及new_category是否为"dummy"
        if template_data.get("component_templates") and new_category == "dummy":
            print(f"Cannot change category to 'dummy' for template '{template_name}' because it has components.")
            return False

        # 根据模板名称更新模板类别
        update_result = cls.db.templates.update_one(
            {"name": template_name},
            {"$set": {"category": new_category}}
        )

        if update_result.modified_count > 0:
            print(f"Template '{template_name}' category changed to '{new_category}'.")
            return True
        else:
            # 由于已经找到了模板，这里不更新可能是因为新旧category相同
            print(f"No changes made to the category of template '{template_name}'.")
            return False

    @classmethod
    def create_element(cls, template_name, properties=None, position=None, component_of=None, create_components=False):
        # 查找模板ID
        template_data = cls.db.templates.find_one({"name": template_name})
        if not template_data:
            print(f"Template '{template_name}' not found.")
            return None

        template_id = template_data.get("template_id")
        new_element = Element(
            element_id=str(uuid.uuid4()),
            template_id=template_id,
            properties=properties,
            position=position,
            components=[],  # 初始化components为空列表
            component_of=component_of
        )

        # 如果需要创建components并且存在component_templates
        if create_components and "component_templates" in template_data:
            for component_template in template_data["component_templates"]:
                component_elements_ids = []  # 存储此组件模板创建的所有元素的ID
                for pos in range(component_template["quantity"]):
                    # 这里假设有一个根据template_id找到template_name的方法
                    component_template_name = cls.get_template_by_id(component_template["element_template_id"]).name
                    component_element_id = cls.create_element(
                        template_name=component_template_name,
                        properties={},  # 可以根据需要传递适当的属性
                        position=pos,
                        component_of=new_element.element_id,
                        create_components=False  # 防止递归创建子组件
                    )
                    if component_element_id:
                        component_elements_ids.append(component_element_id)

                # 将组件模板和对应创建的元素ID列表添加到new_element的components中
                if component_elements_ids:
                    new_element.components.append({
                        "element_template_id": component_template["element_template_id"],
                        "quantity": component_template["quantity"],
                        "component_elements": component_elements_ids
                    })

        # 将完成的Element保存到数据库
        cls.db.elements.insert_one(new_element.to_dict())
        print(f"New element created for template '{template_name}' with ID {new_element.element_id}.")
        return new_element.element_id

    @classmethod
    def find_elements_by_template_name(cls, template_name):
        template_id = cls.get_template_id_by_name(template_name)
        if template_id:
            elements = cls.db.elements.find({"template_id": template_id})
            return list(elements)
        else:
            return []

    @classmethod
    def find_elements_by_template_id(cls, template_id):
        elements = cls.db.elements.find({"template_id": template_id})
        return list(elements)
