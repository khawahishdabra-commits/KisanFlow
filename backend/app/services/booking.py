from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.centre import Centre
from app.models.crop import Crop
from app.models.farmer import Farmer
from app.repositories.booking import BookingRepository
from app.schemas.booking import BookingCreate, BookingResponse


class BookingService:

    def __init__(
        self,
        repository: BookingRepository,
        db: Session,
    ):
        self.repository = repository
        self.db = db

    def create_booking(
        self,
        data: BookingCreate,
        farmer: Farmer,
    ) -> BookingResponse:

        centre = self.db.scalar(
            select(Centre).where(
                Centre.id == data.centre_id
            )
        )

        if not centre:
            raise HTTPException(
                status_code=404,
                detail="Centre not found",
            )

        crop = self.db.scalar(
            select(Crop).where(
                Crop.id == data.crop_id
            )
        )

        if not crop:
            raise HTTPException(
                status_code=404,
                detail="Crop not found",
            )

        booking = Booking(
            farmer_id=farmer.id,
            centre_id=data.centre_id,
            crop_id=data.crop_id,
            booking_date=data.booking_date,
            slot_time=data.slot_time,
            quantity=data.quantity,
            status="BOOKED",
        )

        created_booking = self.repository.create(
            booking
        )

        return BookingResponse.model_validate(
            created_booking
        )

    def get_booking(
        self,
        booking_id: int,
        farmer: Farmer,
    ) -> BookingResponse:

        booking = self.repository.get_by_id_for_farmer(
            booking_id=booking_id,
            farmer_id=farmer.id,
        )

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found",
            )

        return BookingResponse.model_validate(
            booking
        )

    def get_farmer_bookings(
        self,
        farmer_id: int,
    ) -> list[BookingResponse]:

        bookings = self.repository.get_by_farmer(
            farmer_id
        )

        return [
            BookingResponse.model_validate(booking)
            for booking in bookings
        ]