from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_farmer
from app.core.database import get_db
from app.models.farmer import Farmer
from app.schemas.auth import FarmerResponse
from app.schemas.farmer import FarmerUpdate
from app.services.farmer import FarmerService


router = APIRouter(
    prefix="/api/farmers",
    tags=["Farmers"],
)


def get_farmer_service(
    db: Session = Depends(get_db),
) -> FarmerService:
    return FarmerService(db)


@router.get(
    "/me",
    response_model=FarmerResponse,
)
def get_my_profile(
    farmer: Farmer = Depends(get_current_farmer),
):
    return farmer


@router.put(
    "/me",
    response_model=FarmerResponse,
)
def update_my_profile(
    data: FarmerUpdate,
    farmer: Farmer = Depends(get_current_farmer),
    service: FarmerService = Depends(
        get_farmer_service
    ),
):
    return service.update_profile(
        farmer,
        data,
    )