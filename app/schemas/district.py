from typing import List
from pydantic import BaseModel


class DistrictCreateSchema(BaseModel):
    name: str
    region: str


class DistrictSchema(BaseModel):
    _id: str
    name: str


class DistrictsSchema(BaseModel):
    districts: List[DistrictSchema]
