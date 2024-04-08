# coding: utf-8
from .event import Event
from .database_controller import DataBaseController


class EventController(DataBaseController):
    @staticmethod
    def handle_event(event):
        print(f"Handling event: {event.name} with data: {event.data}")

    @classmethod
    def event_wrapper(cls, category, event_type):
        def decorator(func):
            def wrapper(*args, **kwargs):
                # 调用原始函数
                result = func(*args, **kwargs)
                # 构造事件数据
                event_data = {
                    'result': result
                    # 这里可以添加更多的上下文信息，如果需要
                }
                # Create Event
                event = Event(category, event_type, event_data)
                # 保存事件到数据库

                cls.db[event.collection].insert_one(event.to_dict())

                return result

            return wrapper

        return decorator
