import re

from pydantic import BaseModel, ConfigDict, field_validator


class QueryRequest(BaseModel):
    cadastre_number: str
    latitude: float
    longitude: float

    @field_validator("cadastre_number")
    def validate_cadastre_number(cls, value):
        pattern = r"^\d{2}:\d{2}:\d{6,7}:\d{1,8}$"
        if not re.match(pattern, value):
            raise ValueError("Invalid cadastre number format. Expected format: XX:XX:XXXXXXX:XXXX")
        return value

    @field_validator("latitude")
    def validate_latitude(cls, value):
        if not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return value

    @field_validator("longitude")
    def validate_longitude(cls, value):
        if not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return value


class QueryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    cadastre_number: str
    latitude: float
    longitude: float
    result: bool
    created_at: str


class PingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: str
