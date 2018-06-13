from peewee import SqliteDatabase, Model, TextField, BooleanField, CharField, ForeignKeyField, IntegerField, IntegrityError


database = SqliteDatabase('vote.sqlite')


class Team(Model):
    name = CharField(unique=True)
    voteable = BooleanField(default=True)
    members = IntegerField(default=3)

    class Meta:
        database = database


class Vote(Model):
    team = ForeignKeyField(Team, backref='votes')
    idea = ForeignKeyField(Team, backref='idea_votes')
    implementation = ForeignKeyField(Team, backref='implementation_votes')
    progress = ForeignKeyField(Team, backref='progress_votes')

    def save(self, *args, **kwargs):
        team = self.team
        if len(team.votes) >= team.members:
            raise IntegrityError('No More votes allowed for team')
        return super().save(*args, **kwargs)

    class Meta:
        database = database
