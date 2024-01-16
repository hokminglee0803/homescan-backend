from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from . import (
    config
)

settings = config.get_settings()

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "application_name": settings.name
    }
