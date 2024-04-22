# coding:utf-8

from gurulab.ticket_controller import TicketController as tc

print(tc.get_all_ticket_templates())

# # 创建 "拆散热片" 的模板
# disassemble_template_id = tc.create_ticket_template(
#     name="Disassemble",
#     initial_state="Pending",
#     state_transitions={
#         "Pending": {
#             "Completed": {
#                 "action": "DisassembleCompleted",
#                 "description": "Disassemble completed"
#             }
#         },
#         "Completed": {}
#     },
#     sub_ticket_creation_triggers={}
# )
#
# # 创建 "清洗" 的模板
# clean_template_id = tc.create_ticket_template(
#     name="Clean",
#     initial_state="Pending",
#     state_transitions={
#         "Pending": {
#             "Completed": {
#                 "action": "CleanCompleted",
#                 "description": "Cleaning completed"
#             }
#         },
#         "Completed": {}
#     },
#     sub_ticket_creation_triggers={}
# )
#
# # 创建 "维修工程师在治具上Debug" 的模板
# debug_on_jig_template_id = tc.create_ticket_template(
#     name="Debug on Jig",
#     initial_state="Pending",
#     state_transitions={
#         "Pending": {
#             "Pass": {
#                 "action": "DebugPass",
#                 "description": "Hashboard is functioning correctly"
#             },
#             "Faulty": {
#                 "action": "DebugFaulty",
#                 "description": "Fault found during debugging"
#             }
#         },
#         "Pass": {},
#         "Faulty": {}
#     },
#     sub_ticket_creation_triggers={}
# )
#
# # 创建 "根据Debug结果更换元器件" 的模板
# replace_components_template_id = tc.create_ticket_template(
#     name="Replace Components",
#     initial_state="Pending",
#     state_transitions={
#         "Pending": {
#             "Success": {
#                 "action": "ComponentReplaced",
#                 "description": "Faulty component successfully replaced"
#             },
#             "Failed": {
#                 "action": "ReplacementFailed",
#                 "description": "Component replacement failed"
#             }
#         },
#         "Success": {},
#         "Failed": {}
#     },
#     sub_ticket_creation_triggers={}
# )
#
# # 创建 "记录报废，当作料板使用" 的模板
# record_scrap_template_id = tc.create_ticket_template(
#     name="Record Scrap",
#     initial_state="Pending",
#     state_transitions={
#         "Pending": {
#             "Completed": {
#                 "action": "Scrapped",
#                 "description": "Hashboard recorded as scrap"
#             }
#         },
#         "Completed": {}
#     },
#     sub_ticket_creation_triggers={}
# )
#
# # 创建 "涂硅脂" 的模板
# apply_thermal_paste_template_id = tc.create_ticket_template(
#     name="Apply Thermal Paste",
#     initial_state="Pending",
#     state_transitions={
#         "Pending": {
#             "Completed": {
#                 "action": "",
#                 "description": "Thermal Paste Applied"
#             }
#         },
#         "Completed": {}
#     },
#     sub_ticket_creation_triggers={}
# )
#
# # 创建 "涂硅脂" 的模板
# tt = tc.create_ticket_template(
#     name="Aging Test",
#     initial_state="Pending",
#     state_transitions={
#         "Pending": {
#             "Faulty": {
#                 "action": "TestFailed",
#                 "description": "Hashboard failed final test"
#             },
#             "Completed": {
#                 "action": "TestPassed",
#                 "description": "Hashboard passed final test"
#             }
#         },
#         "Faulty": {},
#         "Completed": {}
#     },
#     sub_ticket_creation_triggers={}
# )

tt = tc.create_ticket_template(
    name="L9 Hashboard Maintenance Workflow",
    initial_state="Start",
    state_transitions={
        "Start": {
            "Disassembled": {
                "action": "Clean",
                "description": ""
            },
            "Cleaned": {
                "action": "DebugOnJig",
                "description": ""
            },
            "Faulty"
            "Completed": {
                "action": "TestPassed",
                "description": "Hashboard passed final test"
            }
        },

    },
    sub_ticket_creation_triggers={}
)

tt = tc.get_ticket_template_by_name("Disassemble")
# tc.delete_ticket_template(tt.template_id)
print(tt.to_dict())

tt = tc.get_ticket_template_by_name("Debug on Jig")
# tc.delete_ticket_template(tt.template_id)
print(tt.to_dict())

tt = tc.get_ticket_template_by_name("Replace Components")
# tc.delete_ticket_template(tt.template_id)
print(tt.to_dict())

tt = tc.get_ticket_template_by_name("Record Scrap")
# tc.delete_ticket_template(tt.template_id)
print(tt.to_dict())

tt = tc.get_ticket_template_by_name("Apply Thermal Paste")
# tc.delete_ticket_template(tt.template_id)
print(tt.to_dict())

tt = tc.get_ticket_template_by_name("Aging Test")
print(tt.to_dict())
