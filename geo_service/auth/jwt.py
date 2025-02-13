import jwt
import datetime
from core.config import settings


def create_access_token(data: dict):
    """
    Creates JWT-token.
    """
    to_encode = data.copy()
    expire = (
            datetime.datetime.now(datetime.UTC) +
            datetime.timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def decode_access_token(token: str):
    """
    Decodes JWT-token.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
