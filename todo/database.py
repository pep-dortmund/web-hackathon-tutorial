from peewee import (
    SqliteDatabase,
    Model,
    TextField, BooleanField, DateTimeField, ForeignKeyField,
    FixedCharField,
)
from flask_login import UserMixin


database = SqliteDatabase(None)


class MyModel(Model):

    class Meta:
        database = database


class User(MyModel, UserMixin):
    username = TextField()
    password = FixedCharField(max_length=255)

    def get_id(self):
        return str(self.id)


class ToDo(MyModel):
    description = TextField()
    done = BooleanField(default=False)
    due_date = DateTimeField(null=True)
    user = ForeignKeyField(User, related_name='todos')
