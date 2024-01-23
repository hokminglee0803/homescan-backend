from typing import List
from pydantic import BaseModel


class EstateCreateSchema(BaseModel):
    name: str
    district: str


class EstateSchema(BaseModel):
    _id: str
    name: str


class EstatesSchema(BaseModel):
    estates: List[EstateSchema]
