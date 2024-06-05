from datetime import timedelta, datetime

users = {}


class User:
    def __init__(self):
        self.year = None
        self.month = None
        self.day = None
        self.__registration_date = None
        self.__trial_period_start = None
        self.__payment_date = None
        self.__start_date = datetime.now()

    @property
    def start_date(self):
        return self.__start_date

    @property
    def registration_date(self):
        return self.__registration_date

    @property
    def trial_period_start(self):
        return self.__trial_period_start

    @property
    def payment_date(self):
        return self.__payment_date

    @registration_date.setter
    def registration_date(self, value):
        self.__registration_date = value

    @trial_period_start.setter
    def trial_period_start(self, value):
        self.__trial_period_start = value

    @payment_date.setter
    def payment_date(self, value):
        self.__payment_date = value

    def is_legal(self):
        if self.payment_date:
            return True
        if self.trial_period_start is None:
            return False
        trial_end = self.trial_period_start + timedelta(days=3)
        if datetime.now() > trial_end:
            return False
        return True


def add_new_user(user_id):
    if user_id not in users:
        users[user_id] = User()
    else:
        raise Exception("User already exists")


def get_user(user_id):
    if user_id in users:
        return users[user_id]
    else:
        raise Exception("User does not exist")

