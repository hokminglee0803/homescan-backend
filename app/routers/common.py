from typing import List
from fastapi import APIRouter


router = APIRouter(prefix="/common")

@router.get("/regions",response_model=List[Region])
def get_regions():
    return {
        "regions": []
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
    
https://camillovisini.com/coding/abstracting-fastapi-services