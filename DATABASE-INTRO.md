# Quick and dirty database intro

We're using SQL databases (SQLite, to be precise).

SQL is a *relational* Database, meaning that
- Database consists of multiple tables
- Each row is identified by a unique key

We're also using `peewee` which simplifies a lot of the complicated
relational stuff.

```python
import peewee

db = peewee.SqliteDatabase('my_app.db')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class User(BaseModel):
    username = peewee.CharField(unique=True)

class Tweet(BaseModel):
    user = peewee.ForeignKeyField(User, backref='tweets')
    message = peewee.TextField()
```

```python
db.create_tables([User, Tweet], safe=True)
```

```python
new_user = User(username='Kevin')
new_user.id  # user is not yet "committed", aka stored in the db
```

```python
new_user.save()
new_user.id
```

*Table User*

| ID | Username |
|----|----------|
| 1  | Kevin    |

```python
tweet = Tweet(user=new_user, message="Hello")
tweet.save()

Tweet(user=new_user, message="Databases are neat").save()
```

*Table Tweets*

| ID | Message            | User_ID |
|----|--------------------|---------|
| 1  | Hello              | 1       |
| 2  | Databases are neat | 1       |

```python
for t in Tweet.select():
    print(f'"{t.message}" posted from {t.user.username}')
```

Internally, this is performing a join operation with Tweet.User_ID and User.ID.
```python
for t in Tweet.select().join(User):
    print(f'"{t.message}" posted from {t.user.username}')
```
