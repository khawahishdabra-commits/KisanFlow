from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.centre import Centre


class CentreRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Centre]:
        statement = select(Centre).order_by(Centre.id)

        return list(
            self.db.scalars(statement).all()
        )