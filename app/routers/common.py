from typing import List
from fastapi import APIRouter, Request
from app.schemas.region import RegionsSchema

from app.services.region import RegionService

router = APIRouter()
region_service = RegionService()


@router.get("/regions", response_model=RegionsSchema)
def get_regions():
    result = region_service.get_regions()
    return {
        "regions": result
    }


@router.get("/districts")
def get_regions():
    return {
        "districts": []
    }


@router.get("/estate")
def get_regions():
    return {
        "estate": []
    }
