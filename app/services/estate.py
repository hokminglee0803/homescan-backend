from pymongo.collection import Collection
from app.models.estate import EstateModel
from app.schemas.district import DistrictCreateSchema
from app.schemas.estate import EstateCreateSchema
from app.utils.mongodb import get_database


def get_collection() -> Collection:
    database = get_database()
    return database["estates"]


class EstateService():

    def get_estates_by_district(self, district):
        estates = get_collection().find({
            "district": district
        })
        return [EstateModel(**estate) for estate in estates]

    def update_estate(self, value: EstateCreateSchema):
        get_collection().update_one({
            "name": value['name'],
            "district": value['district']
        }, {
            "$set": {
                "name": value['name'],
                "district": value['district']
            }
        }, upsert=True)