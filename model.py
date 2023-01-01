from peewee import *
from datetime import datetime, date, timedelta

db = SqliteDatabase('sample.db')


def initialize():
    with db:
	# database.connect()
        db.connect()
        db.create_tables([Question])
        db.commit()
        db.close()

class Question(Model):
    keyword = TextField()
    explain = TextField()
    chapter = IntegerField(null=False)
    number_of_question = IntegerField(null=False)
    the_number_of_correct_answers = IntegerField(null=False)
    comment = TextField()

    class Meta:
        database = db