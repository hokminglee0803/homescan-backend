from typing import List
from pydantic import BaseModel


class BuildingCreateSchema(BaseModel):
    name: str
    estate: str


class BuildingSchema(BaseModel):
    _id: str
    name: str


class BuildingsSchema(BaseModel):
    buildings: List[BuildingSchema]
