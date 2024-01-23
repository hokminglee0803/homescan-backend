import uuid
from pydantic import BaseModel, Field


class HouseModel(BaseModel):
    _id: str = Field(default_factory=uuid.uuid4, alias="_id")
    region: str = Field(...)
    district: str = Field(...)
    region: str = Field(...)
    estate: str = Field(...)
    building: str = Field(...)
    block: str = Field(...)
    estimation: float = Field(...)

    class Config:
        allow_population_by_field_name = True
