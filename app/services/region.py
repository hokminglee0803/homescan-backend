from pymongo.collection import Collection
from app.models.region import RegionModel
from app.utils.mongodb import get_database


def get_items_collection() -> Collection:
    database = get_database()
    return database["regions"]


class RegionService():

    def get_regions(self):
        regions = get_items_collection().find()
        return [RegionModel(**region) for region in regions]

    def create_regions():
        return []

    def delete_regions():
        return []


https://camillovisini.com/coding/abstracting-fastapi-services
https://www.mongodb.com/languages/python/pymongo-tutorial
https://www.mongodb.com/languages/python