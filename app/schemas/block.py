from typing import List
from pydantic import BaseModel


class BlockCreateSchema(BaseModel):
    floor: str
    block: str
    building: str

class BlocksSchema(BaseModel):
    floors: List[str]
    block: List[str]
