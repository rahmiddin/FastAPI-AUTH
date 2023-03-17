from fastapi import Request, HTTPException, Response, status, FastAPI
from fastapi_users import FastAPIUsers
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from database.models import get_user_db
from database.models import User, create_db_and_tables, Shop
from user.schemas import UserRead, UserUpdate, UserCreate, ShopCreate
from user.manager import auth_backend, get_user_manager
from database.models import get_async_session

API = FastAPI(
    title="App",
)


@API.on_event("startup")
async def on_startup():
    # Not needed if you setup a migrations system like Alembic
    await create_db_and_tables()


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


API.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"],
)
API.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/user/jwt",
    tags=["user"],
)
API.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/user",
    tags=["user"],
)
API.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/user",
    tags=["user"],
)
API.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/user",
    tags=["user"],
)


