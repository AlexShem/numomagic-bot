from aiogram.types import User


class Action:
    def __init__(self, action: str, user: User, extra=None):
         self.user_id = user.id
         self.username = user.username
         self.first_name = user.first_name
         self.last_name = user.last_name
         self.is_premium = user.is_premium
         self.app_language = user.language_code
         self.action = action
         self.extra = extra

    def __str__(self):
        return ','.join(f'{value}' for _, value in vars(self).items())
