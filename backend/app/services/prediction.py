class PredictionService:

    @staticmethod
    def predict_eta(
        queue_length: int,
        avg_service_time: float,
        active_units: int,
        weather_factor: float = 1.0,
        workload_factor: float = 1.0,
        resource_factor: float = 1.0,
    ) -> float:

        if active_units <= 0:
            return float("inf")

        base_eta = (
            queue_length * avg_service_time
        ) / active_units

        adjusted_eta = (
            base_eta
            * weather_factor
            * workload_factor
            * resource_factor
        )

        return round(adjusted_eta, 2)

    @staticmethod
    def predict_congestion(
        queue_length: int,
        capacity_per_hour: int,
    ) -> str:

        if capacity_per_hour <= 0:
            return "CRITICAL"

        ratio = queue_length / capacity_per_hour

        if ratio < 0.5:
            return "LOW"

        if ratio < 0.8:
            return "MODERATE"

        if ratio <= 1.0:
            return "HIGH"

        return "CRITICAL"

    @staticmethod
    def predict_workload(
        current_bookings: int,
        expected_walk_ins: int,
        historical_average: int,
        context_factor: float = 1.0,
    ) -> float:

        if (
            current_bookings < 0
            or expected_walk_ins < 0
            or historical_average < 0
        ):
            raise ValueError(
                "Workload inputs cannot be negative"
            )

        if context_factor <= 0:
            raise ValueError(
                "Context factor must be greater than zero"
            )

        base_workload = (
            current_bookings
            + expected_walk_ins
            + historical_average
        )

        predicted_workload = (
            base_workload * context_factor
        )

        return round(predicted_workload, 2)