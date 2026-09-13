from app.repositories.crop import CropRepository
from app.schemas.crop import CropResponse


class CropService:

    def __init__(self, repository: CropRepository):
        self.repository = repository

    def get_all_crops(self) -> list[CropResponse]:
        crops = self.repository.get_all()

        return [
            CropResponse.model_validate(crop)
            for crop in crops
        ]