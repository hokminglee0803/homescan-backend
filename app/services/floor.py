from pymongo.collection import Collection
from app.models.floor import FloorModel
from app.schemas.floor import FloorCreateSchema
from app.utils.mongodb import get_database


def get_collection() -> Collection:
    database = get_database()
    return database["floors"]


class FloorService():

    def get_floors(self):
        floors = get_collection().find()
        return [FloorModel(**floor) for floor in floors]

    def update_floor(self, value: FloorCreateSchema):
        get_collection().update_one({
            "name": value['name'],
            "building": value['building']
        }, {
            "$set": {
                "name": value['name'],
                "building": value['building']
            }
        }, upsert=True)
