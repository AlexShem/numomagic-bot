import os

from dotenv import load_dotenv
from peewee import SqliteDatabase, Model

load_dotenv()

db_path = os.getenv("DB_PATH")
db_path = os.path.join(db_path, "users.db")
connection = SqliteDatabase(db_path)
connection.connect()

class BaseModel(Model):
    class Meta:
        database = connection
