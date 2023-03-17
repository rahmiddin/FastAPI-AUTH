from typing import Optional
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy, CookieTransport
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from database.models import User, get_user_db, get_async_session
from user.send_code_on_email import send_verification_code_message
from config import SECRET_KEY

SECRET = SECRET_KEY

cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """FastAPI-users special class to manage users"""

    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        ...

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        ...

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        await send_verification_code_message(recipients=[user.email], jwt=token)

    async def on_after_verify(
            self, user: User, request: Optional[Request] = None,
    ):
        ...


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="user/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
