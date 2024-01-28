import uuid
from pydantic import BaseModel, Field
class HouseModel(BaseModel):
    _id: str = Field(default_factory=uuid.uuid4, alias="_id")
    address: str = Field(...)
    region: str = Field(...)
    district: str = Field(...)
    estate: str = Field(...)
    building: str = Field(...)
    floor: str = Field(...)
    block: str = Field(...)
    hsbc_valuation: str = Field(...)
    hsb_valuation: str = Field(...)
    gross_floor_area: str 
    saleable_area: str
    property_age: str 
    date_completion: str

    class Config:
        allow_population_by_field_name = True
