from fastapi import FastAPI
from database import database as connection

from database import User
from database import Movie
from database import UserReview

from schemas import UserBaseModel

app = FastAPI(title='Proyecto para reseniar peliculas',
            description='En este proyecto seremos capaces de reseniar peliculas',
            version='1')

@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()

        print('Connecting...')
    
    connection.create_tables([User, Movie, UserReview])

@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
        
        print('Closed')


@app.get('/')
async def index():
    return 'Hola Mundo, desde un servidor en FastAPI'

@app.get('/about')
async def about():
    return 'About'

@app.post('/user/')
async def create_user(user: UserBaseModel):
    user = User.create(
        username=user.username,
        password=user.password
    )

    return user.id
