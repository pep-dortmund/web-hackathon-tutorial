from peewee import SqliteDatabase, Model, TextField, BooleanField


database = SqliteDatabase('todo.sqlite')


class ToDo(Model):
    description = TextField()
    done = BooleanField(default=False)

    class Meta:
        database = database
