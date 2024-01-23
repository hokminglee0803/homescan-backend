from fastapi import APIRouter
from app.schemas.house import HouseSchema

from app.services.region import RegionService

router = APIRouter()
region_service = RegionService()


@router.get("/detail", response_model=HouseSchema)
def get_house_detail():
    return {}
