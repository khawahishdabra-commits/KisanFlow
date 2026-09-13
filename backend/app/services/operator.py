from fastapi import HTTPException

from app.repositories.intelligence import IntelligenceRepository
from app.schemas.operator import (
    OperatorCentre,
    OperatorDashboardResponse,
    OperatorPredictions,
    OperatorQueue,
    OperatorResource,
)
from app.services.prediction import PredictionService
from app.services.resource_recommendation import (
    ResourceRecommendationService,
)
from app.services.simulation import SimulationService

class OperatorDashboardService:

    def __init__(
        self,
        repository: IntelligenceRepository,
    ):
        self.repository = repository

    def get_dashboard(
        self,
        centre_id: int,
    ) -> OperatorDashboardResponse:

        centre = self.repository.get_centre(
            centre_id
        )

        if not centre:
            raise HTTPException(
                status_code=404,
                detail="Centre not found",
            )

        queue = self.repository.get_queue(
            centre_id
        )

        if not queue:
            raise HTTPException(
                status_code=404,
                detail="Queue data not found for this centre",
            )

        resources = self.repository.get_resources(
            centre_id
        )

        active_units = sum(
            resource.available_units
            for resource in resources
            if resource.status == "AVAILABLE"
        )

        eta_minutes = PredictionService.predict_eta(
            queue_length=queue.queue_length,
            avg_service_time=queue.avg_service_time,
            active_units=active_units,
        )

        congestion = PredictionService.predict_congestion(
            queue_length=queue.queue_length,
            capacity_per_hour=centre.capacity_per_hour,
        )

        predicted_workload = PredictionService.predict_workload(
            current_bookings=0,
            expected_walk_ins=10,
            historical_average=20,
        )

        return OperatorDashboardResponse(
            centre=OperatorCentre(
                id=centre.id,
                name=centre.name,
            ),
            queue=OperatorQueue(
                current_queue=queue.queue_length,
                estimated_wait_minutes=queue.estimated_wait_minutes,
            ),
            predictions=OperatorPredictions(
                eta_minutes=eta_minutes,
                congestion=congestion,
                predicted_workload=predicted_workload,
            ),
            resources=[
                OperatorResource(
                    type=resource.resource_type,
                    total=resource.total_units,
                    available=resource.available_units,
                    status=resource.status,
                )
                for resource in resources
            ],
        )

    def get_resource_recommendation(self, centre_id: int):

        centre = self.repository.get_centre(centre_id)

        if not centre:
            raise HTTPException(
                status_code=404,
                detail="Centre not found",
            )

        queue = self.repository.get_queue(centre_id)

        if not queue:
            raise HTTPException(
                status_code=404,
                detail="Queue data not found for this centre",
            )

        resources = self.repository.get_resources(centre_id)

        active_units = sum(
            resource.available_units
            for resource in resources
            if resource.status == "AVAILABLE"
        )

        eta_minutes = PredictionService.predict_eta(
            queue_length=queue.queue_length,
            avg_service_time=queue.avg_service_time,
            active_units=active_units,
        )

        recommendation = ResourceRecommendationService.recommend(
            queue_length=queue.queue_length,
            eta_minutes=eta_minutes,
            resources=resources,
        )

        if recommendation is None:
            return {
                "centre_id": centre_id,
                "recommendation": None,
            }

        return {
            "centre_id": centre_id,
            "recommendation": {
                "resource_type": recommendation.resource_type,
                "recommended_change": recommendation.recommended_change,
                "reason": recommendation.reason,
            },
        }

    def simulate_resource_change(
        self,
        centre_id: int,
        resource_type: str,
        resource_change: int,
    ):
        centre = self.repository.get_centre(centre_id)

        if not centre:
            raise HTTPException(
                status_code=404,
                detail="Centre not found",
            )

        queue = self.repository.get_queue(centre_id)

        if not queue:
            raise HTTPException(
                status_code=404,
                detail="Queue data not found for this centre",
            )

        resources = self.repository.get_resources(centre_id)

        active_units = sum(
            resource.available_units
            for resource in resources
            if resource.status == "AVAILABLE"
        )

        if active_units <= 0:
            raise HTTPException(
                status_code=400,
                detail="Centre has no active processing units",
            )

        result = SimulationService.simulate(
            queue_length=queue.queue_length,
            avg_service_time=queue.avg_service_time,
            active_units=active_units,
            resource_type=resource_type,
            resource_change=resource_change,
        )

        return {
            "centre_id": centre_id,
            "resource_type": result.resource_type,
            "resource_change": result.resource_change,
            "before_queue": result.before_queue,
            "after_queue": result.after_queue,
            "before_wait": result.before_wait,
            "after_wait": result.after_wait,
        }