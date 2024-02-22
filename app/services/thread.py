from pymongo.collection import Collection
from app.models.thread import ThreadModel
from app.schemas.thread import ThreadCreateSchema
from app.utils.mongodb import get_database


def get_collection() -> Collection:
    database = get_database()
    return database["threads"]


class ThreadService():

    def get_threads(self,thread_idx:str):
        thread = get_collection().find_one({
            "thread_idx":thread_idx
        })
        return ThreadModel(**thread)

    def update_thread(self, value: ThreadCreateSchema):
        get_collection().update_one({
            "thread_idx":value['thread_idx']
        }, {
            "$set": {
                "region_idx": value['region_idx'],
                "district_idx": value['district_idx'],
                "estate_idx": value['estate_idx'],
                "building_idx": value['building_idx'],
                "floor_idx": value['floor_idx'],
                "block_idx": value['block_idx'],
            }
        }, upsert=True)
