from app.repositories.centre import CentreRepository
from app.schemas.centre import CentreResponse


class CentreService:

    def __init__(self, repository: CentreRepository):
        self.repository = repository

    def get_all_centres(self) -> list[CentreResponse]:
        centres = self.repository.get_all()

        return [
            CentreResponse.model_validate(centre)
            for centre in centres
        ]