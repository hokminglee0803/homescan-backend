from typing import List
from pydantic import BaseModel


class HouseCreateSchema(BaseModel):
    valuation: str
    region: str
    district: str
    estate: str
    building: str
    floor: str
    block: str
    gross_floor_area: str
    saleable_area: str
    property_age: str


class HouseSchema(BaseModel):
    _id: str
    value: float
    region: str
    district: str
    estate: str
    building: str
    floor: str
    block: str
