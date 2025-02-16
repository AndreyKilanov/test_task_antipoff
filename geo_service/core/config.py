import os
from pathlib import Path

from dotenv import load_dotenv


path = Path(__file__).parent.parent.parent / '.env' # del 1 parent for docker
load_dotenv(path)


DEFAULT_TITLE_APP = 'Geo Service'
DEFAULT_APP_DESCRIPTION = 'API for working with geo data.'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=30


class Settings:
    # App
    app_title: str = os.getenv('APP_TITLE', DEFAULT_TITLE_APP)
    app_description: str = os.getenv('APP_DESCRIPTION', DEFAULT_APP_DESCRIPTION)

    # Postgres
    postgres_user: str = os.getenv('POSTGRES_USER')
    postgres_password: str = os.getenv('POSTGRES_PASSWORD')
    postgres_db: str = os.getenv('POSTGRES_DB')
    db_container_name: str = os.getenv('POSTGRES_CONTAINER_NAME')
    postgres_port: str = os.getenv('POSTGRES_PORT')
    database_url: str = (
        f'postgresql+asyncpg://{postgres_user}:{postgres_password}@'
        f'{db_container_name}:{postgres_port}/{postgres_db}'
    )
    # database_url: str = (
    #     f'postgresql+asyncpg://{postgres_user}:{postgres_password}@'
    #     f'localhost:{postgres_port}/{postgres_db}'
    # )

    # Users
    secret_key: str = os.getenv('SECRET_KEY')
    algorithm: str = os.getenv('ALGORITHM', ALGORITHM)
    access_token_expire_minutes: int = int(
        os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Admin
    admin_username: str = os.getenv('ADMIN_USERNAME')
    admin_password: str = os.getenv('ADMIN_PASSWORD')

    # Mock server
    mock_server_port: str = os.getenv('MOCK_SERVER_PORT')
    mock_server_host: str = os.getenv('MOCK_SERVER_HOST')

settings = Settings()
