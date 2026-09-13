from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.intelligence import IntelligenceRepository
from app.schemas.intelligence import CentreIntelligenceResponse
from app.services.intelligence import IntelligenceService


router = APIRouter(
    prefix="/api/centres",
    tags=["Centre Intelligence"],
)


def get_intelligence_service(
    db: Session = Depends(get_db),
) -> IntelligenceService:
    repository = IntelligenceRepository(db)

    return IntelligenceService(repository)


@router.get(
    "/{centre_id}/intelligence",
    response_model=CentreIntelligenceResponse,
)
def get_centre_intelligence(
    centre_id: int,
    service: IntelligenceService = Depends(
        get_intelligence_service
    ),
):
    return service.get_centre_intelligence(centre_id)