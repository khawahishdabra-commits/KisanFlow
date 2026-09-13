from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.centre import CentreRepository
from app.schemas.centre import CentreResponse
from app.services.centre import CentreService


router = APIRouter(
    prefix="/api/centres",
    tags=["Centres"],
)


def get_centre_service(
    db: Session = Depends(get_db),
) -> CentreService:
    repository = CentreRepository(db)

    return CentreService(repository)


@router.get(
    "",
    response_model=list[CentreResponse],
)
def get_centres(
    service: CentreService = Depends(get_centre_service),
):
    return service.get_all_centres()