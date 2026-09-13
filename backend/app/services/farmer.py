from sqlalchemy.orm import Session

from app.models.farmer import Farmer
from app.schemas.farmer import FarmerUpdate


class FarmerService:

    def __init__(self, db: Session):
        self.db = db

    def update_profile(
        self,
        farmer: Farmer,
        data: FarmerUpdate,
    ) -> Farmer:

        if data.name is not None:
            farmer.name = data.name

        if data.language is not None:
            farmer.language = data.language

        if data.latitude is not None:
            farmer.latitude = data.latitude

        if data.longitude is not None:
            farmer.longitude = data.longitude

        self.db.commit()
        self.db.refresh(farmer)

        return farmer