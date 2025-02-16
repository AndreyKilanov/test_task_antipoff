import contextlib
from typing import AsyncIterator

from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware

import core
from admin.admin import UserAdmin, RoleAdmin, GeoAdmin
from admin.auth_admin import authentication_backend
from api.routers import main_router
from auth.roles import create_roles
from auth.users import create_admin_user
from core.config import settings


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    core.db_manager.init(settings.database_url)
    await create_roles()
    await create_admin_user()
    yield
    await core.db_manager.close()


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)

admin = Admin(
    app,
    authentication_backend=authentication_backend,
    base_url="/admin",
    title="GEO SERVICE Admin"
)

admin.add_view(UserAdmin)
admin.add_view(RoleAdmin)
admin.add_view(GeoAdmin)
