from pymongo.collection import Collection
from app.models.district import DistrictModel
from app.schemas.district import DistrictCreateSchema
from app.utils.mongodb import get_database


def get_collection() -> Collection:
    database = get_database()
    return database["districts"]


class DistrictService():

    def get_districts_by_region(self, region):
        districts = get_collection().find({
            "region": region
        })
        return [DistrictModel(**district) for district in districts]

    def update_district(self, value: DistrictCreateSchema):
        get_collection().update_one({
            "name": value['name'],
            "region": value['region']
        }, {
            "$set": {
                "name": value['name'],
                "region": value['region']
            }
        }, upsert=True)
