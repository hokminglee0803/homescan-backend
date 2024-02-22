import uuid
from pydantic import BaseModel, Field
class ThreadModel(BaseModel):
    _id: str = Field(default_factory=uuid.uuid4, alias="_id")
    thread_idx:int = Field(...)
    region_idx: int = Field(...)
    district_idx: int = Field(...)
    estate_idx: int = Field(...)
    building_idx: int = Field(...)
    floor_idx: int = Field(...)
    block_idx: int = Field(...)

    class Config:
        allow_population_by_field_name = True
