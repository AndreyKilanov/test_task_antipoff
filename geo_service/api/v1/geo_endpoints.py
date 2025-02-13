import logging
import re
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from api.validators import validate_cadastre_number
from auth.users import get_current_user
from core import get_async_session
from core.config import settings
from models import Geo
from schemas.geo_schemas import QueryResponse, QueryRequest, PingResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix='')

# url_mock_server = f"http://{settings.mock_server_host}:{settings.mock_server_port}"
url_mock_server = f"http://localhost:{settings.mock_server_port}"


@router.post(
    '/query',
    response_model=QueryResponse,
    dependencies=[Depends(get_current_user)],
    name="Query to mock server(Auth only)"
)
async def query(
        query: QueryRequest,
        db: AsyncSession = Depends(get_async_session),
) -> QueryResponse:
    """
    Query to mock server and save to database.\n\n
    Validate query: \n
        - cadastre_number min length (3 characters) and Expected format: XX:XX:XXXXXXX:XXXX"\n
        - latitude max (-90, 90)\n
        - longitude max (-180, 180)\n
    """

    async with httpx.AsyncClient() as client:

        try:

            response = await client.post(
                url_mock_server + "/result",
                json={
                    "cadastre_number": query.cadastre_number,
                    "latitude": query.latitude,
                    "longitude": query.longitude
                },
                timeout=5,
            )
            response.raise_for_status()
            result = response.json().get("result")
            logger.info(f"Query result: {result}")

        except httpx.TimeoutException:
            logger.error("External server timeout")
            raise HTTPException(status_code=504, detail="External server timeout")

        except httpx.HTTPStatusError as e:
            logger.error(e.response.text)
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

    try:
        new_query = Geo(
            cadastre_number=query.cadastre_number,
            latitude=query.latitude,
            longitude=query.longitude,
            result=result,
        )
        db.add(new_query)
        await db.commit()
        await db.refresh(new_query)
        logger.info(f"New query created: {new_query}")

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"An unexpected error occurred while saving to the database: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while saving to the database: {str(e)}"
        )

    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    return QueryResponse(
        id=str(new_query.id),
        cadastre_number=new_query.cadastre_number,
        latitude=new_query.latitude,
        longitude=new_query.longitude,
        result=new_query.result,
        created_at=new_query.created_at.isoformat(), # noqa
    )


@router.get(
    "/ping",
    response_model=PingResponse,
    dependencies=[Depends(get_current_user)],
    name="Ping to mock server(Auth only)"
)
async def ping() -> PingResponse:
    """
    Ping to mock server.
    """
    async with httpx.AsyncClient() as client:

        try:
            response = await client.get(url_mock_server + "/ping")
            return PingResponse(status=response.json().get("status"))

        except httpx.HTTPStatusError as e:
            logger.error(e.response.text)
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.get(
    "/history",
    response_model=list[QueryResponse],
    dependencies=[Depends(get_current_user)],
    name="Get history(Auth only)"
)
async def get_history(db: AsyncSession = Depends(get_async_session))-> list[QueryResponse]:
    """
    Get all history of queries.
    """
    try:

        queries = await db.execute(select(Geo).order_by(Geo.created_at.desc()))

    except SQLAlchemyError as e:
        logger.error(f"An unexpected error occurred while loading the data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while loading the data: {str(e)}"
        )

    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    return [
        QueryResponse(
            id=str(q.id),
            cadastre_number=q.cadastre_number,
            latitude=q.latitude,
            longitude=q.longitude,
            result=q.result,
            created_at=q.created_at.isoformat(), # noqa
        )
        for q in queries.scalars()
    ]


@router.get(
    "/history/{cadastre_number}",
    response_model=QueryResponse,
    dependencies=[Depends(get_current_user)],
    name="Get history by cadastre number(Auth only)"
)
async def get_history_by_cadastre_number(
        cadastre_number: str,
        db: AsyncSession = Depends(get_async_session)
)-> QueryResponse:
    """
    Get history by cadastre number.\n
    Validate cadastre_number: \n
        - format: XX:XX:XXXXXXX:XXXX"\n
    """
    try:

        validate_cadastre_number(cadastre_number)
        query = await db.execute(
            select(Geo)
            .where(Geo.cadastre_number == cadastre_number)
            .order_by(Geo.created_at.desc())
        )

    except SQLAlchemyError as e:
        logger.error(f"An unexpected error occurred while loading the data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while loading the data: {str(e)}"
        )

    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {str(e)}")
    query = query.scalars().first()
    return QueryResponse(
        id=str(query.id),
        cadastre_number=query.cadastre_number,
        latitude=query.latitude,
        longitude=query.longitude,
        result=query.result,
        created_at=query.created_at.isoformat(),
    )
