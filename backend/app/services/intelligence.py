from fastapi import HTTPException

from datetime import date
from app.repositories.intelligence import IntelligenceRepository
from app.schemas.intelligence import (
    CentreIntelligenceResponse,
    PredictionIntelligence,
    QueueIntelligence,
    ResourceIntelligence,
)
from app.services.prediction import PredictionService


class IntelligenceService:

    def __init__(
        self,
        repository: IntelligenceRepository,
    ):
        self.repository = repository

    def get_centre_intelligence(
        self,
        centre_id: int,
    ) -> CentreIntelligenceResponse:

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

        today_booking_count = (
            self.repository.get_today_booking_count(
                centre_id,
                date.today(),
            )
        )

        active_units = sum(
            resource.available_units
            for resource in resources
            if resource.status == "AVAILABLE"
        )

        predicted_workload = (
            PredictionService.predict_workload(
                current_bookings=today_booking_count,
                expected_walk_ins=10,
                historical_average=20,
                context_factor=1.0,
            )
        )

        eta_minutes = PredictionService.predict_eta(
            queue_length=queue.queue_length,
            avg_service_time=queue.avg_service_time,
            active_units=active_units,
        )

        congestion_level = (
            PredictionService.predict_congestion(
                queue_length=queue.queue_length,
                capacity_per_hour=centre.capacity_per_hour,
            )
        )

        return CentreIntelligenceResponse(
            centre_id=centre.id,
            centre_name=centre.name,
            status=centre.status,
            queue=QueueIntelligence(
                queue_length=queue.queue_length,
                avg_service_time=queue.avg_service_time,
                estimated_wait_minutes=queue.estimated_wait_minutes,
            ),
            predictions=PredictionIntelligence(
                eta_minutes=eta_minutes,
                congestion_level=congestion_level,
                predicted_workload=predicted_workload,
            ),
            resources=[
                ResourceIntelligence(
                    resource_type=resource.resource_type,
                    total_units=resource.total_units,
                    available_units=resource.available_units,
                    status=resource.status,
                )
                for resource in resources
            ],
        )