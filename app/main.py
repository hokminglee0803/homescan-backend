from fastapi import FastAPI
from pymongo import MongoClient
from app.routers.common import router as common_router
import app.config
import logging

from app.utils.mongodb import close_mongodb_connection, connect_to_mongodb

settings = app.config.get_settings()

logger = logging.getLogger(__name__)

app = FastAPI()

# @app.exception_handler(AppExceptionCase)
# async def custom_app_exception_handler(request, e):
#     return await app_exception_handler(request, e)


@app.on_event("startup")
def startup_db_client():
    connect_to_mongodb()
    logger.info("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    close_mongodb_connection()


app.include_router(common_router,tags=['Common'],prefix="/common")
