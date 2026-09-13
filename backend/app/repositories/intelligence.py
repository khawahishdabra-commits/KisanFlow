from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.centre import Centre
from app.models.queue import Queue
from app.models.resource import Resource


class IntelligenceRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_centre(
        self,
        centre_id: int,
    ) -> Centre | None:

        return self.db.scalar(
            select(Centre).where(
                Centre.id == centre_id
            )
        )

    def get_queue(
        self,
        centre_id: int,
    ) -> Queue | None:

        return self.db.scalar(
            select(Queue).where(
                Queue.centre_id == centre_id
            )
        )

    def get_resources(
        self,
        centre_id: int,
    ) -> list[Resource]:

        statement = (
            select(Resource)
            .where(
                Resource.centre_id == centre_id
            )
            .order_by(Resource.id)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_today_booking_count(
        self,
        centre_id: int,
        booking_date: date,
    ) -> int:

        statement = (
            select(func.count(Booking.id))
            .where(
                Booking.centre_id == centre_id,
                Booking.booking_date == booking_date,
            )
        )

        return self.db.scalar(statement) or 0