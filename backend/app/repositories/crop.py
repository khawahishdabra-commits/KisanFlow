from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.crop import Crop


class CropRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Crop]:
        statement = select(Crop).order_by(Crop.id)

        return list(
            self.db.scalars(statement).all()
        )