from typing import List
from pydantic import BaseModel


class RegionCreateSchema(BaseModel):
    name: str

class RegionSchema(BaseModel):
    _id: str
    name: str

class RegionsSchema(BaseModel):
    regions: List[RegionSchema]
