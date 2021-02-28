from fastapi import APIRouter

from . import schemas
from .models import User

account_router = APIRouter(prefix='/accounts', tags=['accounts'])

@account_router.get('/')
async def index():
    return {'message': 'This is account index'}

@account_router.post('/register', response_model=schemas.UserRegisterResponse)
async def register(user: schemas.UserRegisterRequest):
    new_user_response = await User.register(user)
    return new_user_response.dict()

@account_router.post('/login')
async def login(user: schemas.UserLoginRequest):
    pass
