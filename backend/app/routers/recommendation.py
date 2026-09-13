from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.centre import CentreRepository
from app.repositories.intelligence import IntelligenceRepository
from app.repositories.price import PriceRepository
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
)
from app.services.recommendation import RecommendationService


router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations"],
)


def get_recommendation_service(
    db: Session = Depends(get_db),
) -> RecommendationService:

    centre_repository = CentreRepository(db)
    price_repository = PriceRepository(db)
    intelligence_repository = IntelligenceRepository(db)

    return RecommendationService(
        centre_repository=centre_repository,
        price_repository=price_repository,
        intelligence_repository=intelligence_repository,
    )


@router.post(
    "/centres",
    response_model=RecommendationResponse,
)
def recommend_centre(
    data: RecommendationRequest,
    service: RecommendationService = Depends(
        get_recommendation_service
    ),
):
    return service.recommend(data)