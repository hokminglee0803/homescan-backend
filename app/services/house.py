from typing import List
from pymongo.collection import Collection
from app.models.building import BuildingModel
from app.models.house import HouseModel
from app.models.region import RegionModel
from app.schemas.building import BuildingCreateSchema
from app.schemas.house import HouseCreateSchema
from app.schemas.region import RegionCreateSchema
from app.utils.mongodb import get_database


def get_collection() -> Collection:
    database = get_database()
    return database["houses"]


class HouseService():

    def get_houses(self):
        houses = get_collection().find()
        return [HouseModel(**house) for house in houses]

    def update_house_hsbc(self, house: HouseCreateSchema):
        get_collection().update_one({
            "region": house['region'],
            "district": house['district'],
            "estate": house['estate'],
            "building": house['building'],
            "floor": house['floor'],
            "block": house['block']
        }, {
            "$set": {
                "hsbc_valuation": house['valuation'],
                "address": f'{house["region"]}{house["district"]}{house["estate"]}{house["building"]}{house["floor"]}{house["block"]}',
                "region": house['region'],
                "district": house['district'],
                "estate": house['estate'],
                "building": house['building'],
                "floor": house['floor'],
                "block": house['block'],
                "gross_floor_area": house['gross_floor_area'],
                "saleable_area": house['saleable_area'],
                "property_age": house['property_age']
            }
        }, upsert=True)
