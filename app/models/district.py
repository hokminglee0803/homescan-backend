import uuid
from pydantic import BaseModel, Field


class DistrictModel(BaseModel):
    _id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    region: str = Field(...)

    class Config:
        allow_population_by_field_name = True
