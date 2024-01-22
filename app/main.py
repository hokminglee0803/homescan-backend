from fastapi import FastAPI
from routers import common

from . import (
    config
)

settings = config.get_settings()

app = FastAPI()

# @app.exception_handler(AppExceptionCase)
# async def custom_app_exception_handler(request, e):
#     return await app_exception_handler(request, e)

app.include_router(common.router)
