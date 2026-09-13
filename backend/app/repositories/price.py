from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.price import Price


class PriceRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_prices_for_crop(
        self,
        crop_id: int,
    ) -> list[Price]:

        statement = (
            select(Price)
            .where(
                Price.crop_id == crop_id,
                Price.effective_date <= date.today(),
            )
            .order_by(Price.centre_id)
        )

        return list(
            self.db.scalars(statement).all()
        )