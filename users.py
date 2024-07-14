import sqlite3
from datetime import timedelta, datetime

connection = sqlite3.connect('db/users.db')
cursor = connection.cursor()

def is_legal(self):
    if self.payment_date:
        return True
    if self.trial_period_start is None:
        return False
    trial_end = self.trial_period_start + timedelta(days=3)
    if datetime.now() > trial_end:
        return False
    return True


def add(user_id, username):
    cursor.execute('INSERT INTO users(id, username, ) VALUES (?, ?)', (user_id, username))


def get(user_id):
    if user_id in users:
        return users[user_id]
    else:
        return None

