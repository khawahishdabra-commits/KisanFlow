from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.farmer import Farmer


class FarmerRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_phone(self, phone: str) -> Farmer | None:
        return self.db.scalar(
            select(Farmer).where(
                Farmer.phone == phone
            )
        )

    def get_by_id(self, farmer_id: int) -> Farmer | None:
        return self.db.scalar(
            select(Farmer).where(
                Farmer.id == farmer_id
            )
        )

    def create(self, farmer: Farmer) -> Farmer:
        self.db.add(farmer)
        self.db.commit()
        self.db.refresh(farmer)

        return farmer