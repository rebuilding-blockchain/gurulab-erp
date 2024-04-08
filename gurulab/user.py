from .data_model import DataModel


class User(DataModel):
    collection = 'users'

    def __init__(self, username, password_hash=None, roles=None):
        self.username = username
        self.password_hash = password_hash
        self.roles = roles if roles else []

    def to_dict(self):
        """
        Convert User instance into a dictionary for database insertion.
        """
        return {
            'username': self.username,
            'password_hash': self.password_hash,
            'roles': self.roles,
        }
