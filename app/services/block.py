from pymongo.collection import Collection
from app.models.block import BlockModel
from app.schemas.block import BlockCreateSchema
from app.utils.mongodb import get_database


def get_collection() -> Collection:
    database = get_database()
    return database["blocks"]


class BlockService():

    def get_blocks(self):
        blocks = get_collection().find()
        return [BlockModel(**block) for block in blocks]

    def update_block(self, value: BlockCreateSchema):
        get_collection().update_one({
            "name": value['name'],
            "floor": value['floor'],
            "building":value['building']
        }, {
            "$set": {
                "name": value['name'],
                "floor": value['floor'],
                "building":value['building']
            }
        }, upsert=True)
