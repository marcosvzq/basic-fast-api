from datetime import datetime
from peewee import *

database = MySQLDatabase('test',
                        user='root',
                        password='',
                        host='localhost',
                        port=3306)

class User(Model):
    username = CharField(max_length=50, unique= True)
    password = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self) -> str:
        return self.username

    class Meta:
        database = database
        table_name = 'users'

class Movie(Model):
    title = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self) -> str:
        return self.title

    class Meta:
        database = database
        table_name = 'movies'

class UserReview(Model):
    user = ForeignKeyField(User, backref='reviews')
    movie = ForeignKeyField(Movie, backref='reviews')
    review = TextField()
    score = IntegerField()
    created_at = DateTimeField(default=datetime.now)

    def __str__(self) -> str:
        return f'{self.user.username} - {self.movie.title}'

    class Meta:
        database = database
        table_name = 'user_reviews'