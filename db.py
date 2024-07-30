import os

from dotenv import load_dotenv
from peewee import SqliteDatabase, Model
load_dotenv()

db_path = os.getenv("DB_PATH")
print(db_path)
connection = SqliteDatabase(os.path.join(db_path, "users.db"))


class BaseModel(Model):
    class Meta:
        database = connection
