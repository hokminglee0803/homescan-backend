from typing import List
from pydantic import BaseModel


class HouseCreateSchema(BaseModel):
    value: float
    region: str
    district: str
    estate: str
    building: str
    floor: str
    block: str


class HouseSchema(BaseModel):
    _id: str
    value: float
    region: str
    district: str
    estate: str
    building: str
    floor: str
    block: str
