import bcrypt
from .user import User
from .role import Role
from .permission import Permission
from .event_controller import EventController
from .database_controller import DataBaseController


class UserController(DataBaseController):
    def __init__(self):
        pass

    @classmethod
    @EventController.event_wrapper(category="user", event_type="register")
    def register(cls, username, password, roles=None):
        if cls.db[User.collection].find_one({"username": username}):
            return False

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User(username, password_hash=password_hash, roles=roles)
        cls.db[User.collection].insert_one(user.to_dict())
        return True

    @classmethod
    @EventController.event_wrapper(category="user",event_type="login")
    def login(cls, username, password):
        user_data = cls.db[User.collection].find_one({"username": username})
        if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data["password_hash"]):
            return True
        return False
