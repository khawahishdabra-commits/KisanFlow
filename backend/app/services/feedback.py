from fastapi import HTTPException

from app.repositories.prediction import PredictionRepository


class FeedbackService:

    def __init__(
        self,
        repository: PredictionRepository,
    ):
        self.repository = repository

    def record_feedback(
        self,
        prediction_id: int,
        actual_value: float,
    ):
        prediction = self.repository.get_by_id(
            prediction_id
        )

        if not prediction:
            raise HTTPException(
                status_code=404,
                detail="Prediction not found",
            )

        if actual_value < 0:
            raise ValueError(
                "Actual value cannot be negative"
            )

        error = round(
            actual_value - prediction.predicted_value,
            2,
        )

        return self.repository.create_feedback(
            prediction_id=prediction_id,
            actual_value=actual_value,
            error=error,
        )