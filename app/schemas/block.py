from typing import List
from pydantic import BaseModel


class BlockCreateSchema(BaseModel):
    name: str
    floor: str
    building: str


class BlockSchema(BaseModel):
    _id: str
    name: str


class BlocksSchema(BaseModel):
    blocks: List[BlockSchema]
