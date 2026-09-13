from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.intelligence import IntelligenceRepository
from app.schemas.operator import OperatorDashboardResponse
from app.services.operator import OperatorDashboardService
from app.schemas.operator import (
    OperatorDashboardResponse,
    OperatorResourceRecommendationResponse,
    SimulationRequest,
    SimulationResponse,
    FeedbackRequest,
    FeedbackResponse,
    PredictionRequest,
    PredictionResponse,
)
from app.repositories.prediction import PredictionRepository
from app.services.feedback import FeedbackService
from app.repositories.prediction import PredictionRepository
from app.services.prediction_record import PredictionRecordService

router = APIRouter(
    prefix="/api/operator",
    tags=["Operator"],
)


def get_operator_dashboard_service(
    db: Session = Depends(get_db),
) -> OperatorDashboardService:

    repository = IntelligenceRepository(db)

    return OperatorDashboardService(
        repository=repository,
    )


@router.get(
    "/dashboard",
    response_model=OperatorDashboardResponse,
)
def get_operator_dashboard(
    centre_id: int,
    service: OperatorDashboardService = Depends(
        get_operator_dashboard_service
    ),
):
    return service.get_dashboard(
        centre_id=centre_id,
    )

@router.get(
    "/resource-recommendation",
    response_model=OperatorResourceRecommendationResponse,
)
def get_resource_recommendation(
    centre_id: int,
    service: OperatorDashboardService = Depends(
        get_operator_dashboard_service
    ),
):
    return service.get_resource_recommendation(
        centre_id=centre_id
    )

@router.post(
    "/simulations",
    response_model=SimulationResponse,
)
def simulate_resource_change(
    data: SimulationRequest,
    service: OperatorDashboardService = Depends(
        get_operator_dashboard_service
    ),
):
    return service.simulate_resource_change(
        centre_id=data.centre_id,
        resource_type=data.resource_type,
        resource_change=data.resource_change,
    )

@router.post(
    "/feedback",
    response_model=FeedbackResponse,
)
def record_prediction_feedback(
    data: FeedbackRequest,
    db: Session = Depends(get_db),
):
    repository = PredictionRepository(db)

    service = FeedbackService(
        repository=repository
    )

    return service.record_feedback(
        prediction_id=data.prediction_id,
        actual_value=data.actual_value,
    )

@router.post(
    "/predictions",
    response_model=PredictionResponse,
)
def record_prediction(
    data: PredictionRequest,
    db: Session = Depends(get_db),
):
    repository = PredictionRepository(db)

    service = PredictionRecordService(
        repository=repository
    )

    return service.record_prediction(
        centre_id=data.centre_id,
        prediction_type=data.prediction_type,
        predicted_value=data.predicted_value,
        confidence=data.confidence,
        prediction_time=data.prediction_time,
        target_time=data.target_time,
        model_version=data.model_version,
    )