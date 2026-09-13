from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.booking import Booking


class BookingRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, booking: Booking) -> Booking:
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)

        return booking

    def get_by_id(self, booking_id: int) -> Booking | None:
        return self.db.scalar(
            select(Booking).where(
                Booking.id == booking_id
            )
        )

    def get_by_id_for_farmer(
        self,
        booking_id: int,
        farmer_id: int,
    ) -> Booking | None:

        return self.db.scalar(
            select(Booking).where(
                Booking.id == booking_id,
                Booking.farmer_id == farmer_id,
            )
        )

    def get_by_farmer(
        self,
        farmer_id: int,
    ) -> list[Booking]:

        statement = (
            select(Booking)
            .where(Booking.farmer_id == farmer_id)
            .order_by(
                Booking.booking_date,
                Booking.slot_time,
            )
        )

        return list(
            self.db.scalars(statement).all()
        )