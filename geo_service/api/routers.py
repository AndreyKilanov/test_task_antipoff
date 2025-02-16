from fastapi import APIRouter
from api.v1 import geo_router, users_router

main_router = APIRouter(prefix='/api', responses={404: {'description': 'Not found'}})

main_router.include_router(
    geo_router,
    prefix='/v1',
    tags=['API GEO SERVICE V1'],
)

main_router.include_router(
    users_router,
    prefix='',
    tags=['Users'],
)
