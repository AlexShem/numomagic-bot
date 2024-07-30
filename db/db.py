from peewee import SqliteDatabase, Model

connection = SqliteDatabase('db/users.db')


class BaseModel(Model):
    class Meta:
        database = connection
