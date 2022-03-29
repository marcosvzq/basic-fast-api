from fastapi import FastAPI
from fastapi import HTTPException

from database import database as connection

from database import User
from database import Movie
from database import UserReview

from schemas import UserRequestModel
from schemas import UserResponseModel

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
async def create_user(user: UserRequestModel, response_model = UserResponseModel):

    if User.select().where(User.username == user.username).exists():
        return HTTPException(409, 'El username ya se encuentra en uso')

    hash_pasword = User.create_password(user.password)

    user = User.create(
        username=user.username,
        password=hash_pasword
    )

    return UserResponseModel(id = user.id, username = user.username)

