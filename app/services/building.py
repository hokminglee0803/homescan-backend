from typing import List
from pymongo.collection import Collection
from app.models.building import BuildingModel
from app.models.region import RegionModel
from app.schemas.building import BuildingCreateSchema
from app.schemas.region import RegionCreateSchema
from app.utils.mongodb import get_database


def get_collection() -> Collection:
    database = get_database()
    return database["buildings"]


class BuildingService():

    def get_buildings(self):
        buildings = get_collection().find()
        return [BuildingModel(**building) for building in buildings]

    def update_building(self, value: BuildingCreateSchema):
        get_collection().update_one({
            "name": value['name'],
            "estate": value['estate']
        }, {
            "$set": {
                "name": value['name'],
                "estate": value['estate']
            }
        }, upsert=True)
