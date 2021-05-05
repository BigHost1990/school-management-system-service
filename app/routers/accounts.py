from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks

from ..dependencies import get_user
from ..utils.email import send_email
from ..models import UserModel, RoleModel
from ..schemas import UserSchema, UserLoginRequest, UserLoginResponse, UserRegisterRequest, UserRegisterResponse, UserRegisterWithRole, RoleEnum


account_router = APIRouter(prefix='/accounts', tags=['accounts'])


@account_router.get('/')
async def index(user: UserSchema = Depends(get_user)):
    return {'message': 'This is accounts route index'}


@account_router.post('/register/student', response_model=UserRegisterResponse)
async def register_for_student(request: UserRegisterRequest, background_tasks: BackgroundTasks):
    """
    Register a user with all the information:

    - **email**: user email, must be unique
    - **password**: user password
    - **username**: optional
    - **fullname**: optional
    """
    await send_email(background_tasks, 'richardagus921@gmail.com',
                     '<p>Sekardayu Hana Pradiani</p>')
    response = await UserModel.register(request, [RoleEnum.STUDENT])
    return response


@account_router.post('/register', response_model=UserRegisterResponse)
async def register_with_role(request: UserRegisterWithRole, user: UserSchema = Depends(get_user)):
    """
    Register a user with all the information:

    - **email**: user email, must be unique
    - **password**: user password
    - **username**: optional
    - **fullname**: optional
    - **role_id**: user's role
    """
    privilage_exception = HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='You are not allowed to create that user')

    if user.role_id == RoleEnum.ADMIN:
        pass
    elif user.role_id == RoleEnum.FACULTY_DEAN and set(request.role_mappings).issubset(RoleModel.roles_list[1:]):
        raise privilage_exception
    elif user.role_id == RoleEnum.HEAD_DEPARTEMENT and set(request.role_mappings).issubset(RoleModel.roles_list[2:]):
        raise privilage_exception
    elif user.role_id == RoleEnum.TEACHER and set(request.role_mappings).issubset(RoleModel.roles_list[3:]):
        raise privilage_exception

    response = await UserModel.register(request)
    return response


@account_router.post('/login', response_model=UserLoginResponse)
async def login(user: UserLoginRequest):
    """
    Login user to get token with these required informations:

    - **email**: user email, must be unique
    - **password**: user password
    """
    response = await UserModel.login(user)
    return response.dict()


@account_router.get('/profile')
async def get_profile(user: UserSchema = Depends(get_user)):
    """
    Get logged in user's data
    """
    return user
