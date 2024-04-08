# coding:utf-8

from gurulab.element_controller import ElementController as ec

print(ec.get_all_templates())

ec.new_element_template(name="L9-Hashboard", category="hashboard")

ec.add_component_templates("L9-Hashboards", "L9-asic", 90)

ec.add_component_templates("L9-Hashboard", "L9-asic", 90)
ec.add_component_templates("L9-Hashboard", "L9-asic", 90)
ec.add_component_templates("L9-Hashboard", "AMS1117-SOT89-3.3V", 5)

ec.change_template_category("L9-Hashboard", "dummy")
ec.change_template_category("L9-Hashboard", "hashboard")
ec.change_template_category("L9-hashboard", "hashboard")
