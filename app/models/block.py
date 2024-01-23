import uuid
from pydantic import BaseModel, Field


class BlockModel(BaseModel):
    _id: str = Field(default_factory=uuid.uuid4, alias="_id")
    floor: str = Field(...)
    block: str = Field(...)
    building: str = Field(...)

    class Config:
        allow_population_by_field_name = True
