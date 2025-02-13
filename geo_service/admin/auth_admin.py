from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from api.validators import validate_user
from core import db_manager
from core.config import settings
from schemas.users_schemas import UserLogin


class AdminAuth(AuthenticationBackend):

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        user = UserLogin(username=username, password=password)

        async with db_manager.session() as session:
            token = await validate_user(user, session, check_admin=True)

        request.session.update({"token": token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        return True


authentication_backend = AdminAuth(secret_key=f"{settings.secret_key}")
