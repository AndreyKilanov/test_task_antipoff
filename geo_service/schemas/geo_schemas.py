from pydantic import BaseModel, ConfigDict


class QueryRequest(BaseModel):
    cadastre_number: str
    latitude: float
    longitude: float



class QueryResponse(QueryRequest):
    model_config = ConfigDict(from_attributes=True)

    result: bool
    created_at: str
