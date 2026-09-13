from datetime import datetime

from app.repositories.prediction import PredictionRepository


class PredictionRecordService:

    def __init__(self, repository: PredictionRepository):
        self.repository = repository

    def record_prediction(
        self,
        centre_id: int,
        prediction_type: str,
        predicted_value: float,
        confidence: float | None,
        prediction_time: datetime,
        target_time: datetime,
        model_version: str = "rule-v1",
    ):
        if predicted_value < 0:
            raise ValueError(
                "Predicted value cannot be negative"
            )

        if not prediction_type.strip():
            raise ValueError(
                "Prediction type cannot be empty"
            )

        if not model_version.strip():
            raise ValueError(
                "Model version cannot be empty"
            )

        return self.repository.create_prediction(
            centre_id=centre_id,
            prediction_type=prediction_type,
            predicted_value=predicted_value,
            confidence=confidence,
            prediction_time=prediction_time,
            target_time=target_time,
            model_version=model_version,
        )