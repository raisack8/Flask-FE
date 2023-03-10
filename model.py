from peewee import *
from datetime import datetime, date, timedelta
from setting import SetDb

db = SqliteDatabase(SetDb.DB)

# db = SqliteDatabase('db_product.db')


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

    @classmethod
    def get_specific_chapter(cls, chapter_num):
        try:
            return cls.select().where(
                cls.chapter == chapter_num
            )
        except:
            return None

    class Meta:
        database = db