from typing import List
from pymongo.collection import Collection
from app.models.region import RegionModel
from app.schemas.region import RegionCreateSchema
from app.utils.mongodb import get_database


def get_collection() -> Collection:
    database = get_database()
    return database["regions"]


class RegionService():

    def get_regions(self):
        regions = get_collection().find()
        return [RegionModel(**region) for region in regions]

    def update_region(self, region: RegionCreateSchema):
        get_collection().update_one({
            "name": region,
        }, {
            "$set": {
                "name": region,
            }
        }, upsert=True)
