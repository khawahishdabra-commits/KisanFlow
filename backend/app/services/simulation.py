from dataclasses import dataclass

from app.services.prediction import PredictionService


@dataclass
class SimulationResult:
    resource_type: str
    resource_change: int

    before_queue: int
    after_queue: int

    before_wait: float
    after_wait: float


class SimulationService:

    @staticmethod
    def simulate(
        queue_length: int,
        avg_service_time: float,
        active_units: int,
        resource_type: str,
        resource_change: int,
    ) -> SimulationResult:

        if queue_length < 0:
            raise ValueError("Queue length cannot be negative")

        if avg_service_time <= 0:
            raise ValueError(
                "Average service time must be greater than zero"
            )

        if active_units <= 0:
            raise ValueError(
                "Active processing units must be greater than zero"
            )

        if resource_change <= 0:
            raise ValueError(
                "Resource change must be greater than zero"
            )

        before_wait = PredictionService.predict_eta(
            queue_length=queue_length,
            avg_service_time=avg_service_time,
            active_units=active_units,
        )

        simulated_units = active_units + resource_change

        after_wait = PredictionService.predict_eta(
            queue_length=queue_length,
            avg_service_time=avg_service_time,
            active_units=simulated_units,
        )

        # For MVP, assume the queue itself does not disappear.
        # The increased processing capacity reduces waiting time.
        after_queue = round(
            queue_length * after_wait / before_wait
        )

        return SimulationResult(
            resource_type=resource_type,
            resource_change=resource_change,
            before_queue=queue_length,
            after_queue=after_queue,
            before_wait=before_wait,
            after_wait=after_wait,
        )