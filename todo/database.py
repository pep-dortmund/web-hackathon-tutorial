from peewee import SqliteDatabase, Model, TextField, BooleanField, DateTimeField


database = SqliteDatabase(None)


class ToDo(Model):
    description = TextField()
    done = BooleanField(default=False)
    due_date = DateTimeField(null=True)

    class Meta:
        database = database
