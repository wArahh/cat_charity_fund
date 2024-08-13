from fastapi import APIRouter

from app.core.user import auth_backend, fastapi_users
from app.users.serializers import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt', tags=['Auth']
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth', tags=['Auth']
)
users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [
    rout for rout in users_router.routes if rout.name != 'users:delete_user'
]
router.include_router(
    users_router,
    prefix='/users',
    tags=['users'],
)