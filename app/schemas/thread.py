from typing import List
from pydantic import BaseModel


class ThreadCreateSchema(BaseModel):
    thread_idx: int
    region_idx: int
    district_idx: int
    estate_idx: int
    building_idx: int
    floor_idx: int
    block_idx: int


class ThreadSchema(BaseModel):
    _id: str
    thread_idx: int
    region_idx: int
    district_idx: int
    estate_idx: int
    building_idx: int
    floor_idx: int
    block_idx: int
