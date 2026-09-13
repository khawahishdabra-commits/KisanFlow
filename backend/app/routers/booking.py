from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_farmer
from app.core.database import get_db
from app.models.farmer import Farmer
from app.repositories.booking import BookingRepository
from app.schemas.booking import (
    BookingCreate,
    BookingResponse,
)
from app.services.booking import BookingService


router = APIRouter(
    prefix="/api/bookings",
    tags=["Bookings"],
)


def get_booking_service(
    db: Session = Depends(get_db),
) -> BookingService:

    repository = BookingRepository(db)

    return BookingService(
        repository=repository,
        db=db,
    )


@router.post(
    "",
    response_model=BookingResponse,
    status_code=201,
)
def create_booking(
    data: BookingCreate,
    farmer: Farmer = Depends(get_current_farmer),
    service: BookingService = Depends(
        get_booking_service
    ),
):
    return service.create_booking(
        data,
        farmer,
    )


@router.get(
    "",
    response_model=list[BookingResponse],
)
def get_my_bookings(
    farmer: Farmer = Depends(get_current_farmer),
    service: BookingService = Depends(
        get_booking_service
    ),
):
    return service.get_farmer_bookings(
        farmer.id
    )


@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
)
def get_booking(
    booking_id: int,
    farmer: Farmer = Depends(get_current_farmer),
    service: BookingService = Depends(
        get_booking_service
    ),
):
    return service.get_booking(
        booking_id,
        farmer,
    )