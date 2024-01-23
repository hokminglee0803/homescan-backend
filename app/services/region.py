from typing import List
from pymongo.collection import Collection
from app.models.region import RegionModel
from app.schemas.region import RegionCreateSchema
from app.utils.mongodb import get_database


def get_items_collection() -> Collection:
    database = get_database()
    return database["regions"]


class RegionService():

    def get_regions(self):
        regions = get_items_collection().find()
        return [RegionModel(**region) for region in regions]

    def create_region(self, region: RegionCreateSchema):
        get_items_collection().insert_one({
            "name": region
        })

    def delete_regions(self):
        get_items_collection().delete_many({})
