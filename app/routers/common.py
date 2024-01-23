from fastapi import APIRouter
from app.schemas.district import DistrictsSchema
from app.schemas.estate import EstatesSchema
from app.schemas.region import RegionsSchema
from app.services.district import DistrictService
from app.services.estate import EstateService

from app.services.region import RegionService

router = APIRouter()
region_service = RegionService()
district_service = DistrictService()
estate_service = EstateService()


@router.get("/regions", response_model=RegionsSchema)
def get_regions():
    result = region_service.get_regions()
    return {
        "regions": result
    }


@router.get("/districts", response_model=DistrictsSchema)
def get_districts(region: str):
    result = district_service.get_districts_by_region(region=region)
    return {
        "districts": result
    }


@router.get("/estate", response_model=EstatesSchema)
def get_estates(district: str):
    result = estate_service.get_estates_by_district(district=district)
    return {
        "estates": result
    }
