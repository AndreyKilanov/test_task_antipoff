from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserProfile(BaseModel):
    username: str
    role: str
    created_at: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str
