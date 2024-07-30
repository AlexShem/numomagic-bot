from datetime import timedelta, datetime
from peewee import TextField, DoesNotExist, PrimaryKeyField, IntegerField
from db import BaseModel


class User(BaseModel):
    id = PrimaryKeyField(column_name='id')
    username = TextField(column_name='username', null=True)
    trial_start = TextField(column_name='trial_start', null=True)
    payment = IntegerField(column_name='payment', null=True)

    class Meta:
        table_name = 'users'

    def is_legal(self):
        if self.payment is not None:
            return True
        if self.trial_start is None:
            return False
        trial_start = datetime.strptime(self.trial_start, '%Y-%m-%d')
        trial_end = trial_start + timedelta(days=2)
        if datetime.now() > trial_end:
            return False
        return True

    def start_trial(self):
        if self.trial_start is None:
            now = str(datetime.now().strftime('%Y-%m-%d'))
            self.trial_start = now
            self.save()
            return True
        return False

    def pay(self):
        self.payment = 1
        self.save()


def add(user_id, username=None):
    User.create(id=user_id, username=username, trial_start=None)


def get(user_id) -> User:
    user = None
    try:
        user = User.get(User.id == user_id)
    except DoesNotExist:
        pass
    return user
