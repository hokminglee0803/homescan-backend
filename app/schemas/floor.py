from typing import List
from pydantic import BaseModel


class FloorCreateSchema(BaseModel):
    name: str
    building: str


class FloorSchema(BaseModel):
    _id: str
    name: str


class FloorsSchema(BaseModel):
    floors: List[FloorSchema]
