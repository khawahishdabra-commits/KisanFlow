from datetime import datetime

from sqlalchemy.orm import Session

from app.models.feedback import Feedback
from app.models.prediction import Prediction


class PredictionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_prediction(
        self,
        centre_id: int,
        prediction_type: str,
        predicted_value: float,
        confidence: float | None,
        prediction_time: datetime,
        target_time: datetime,
        model_version: str,
    ) -> Prediction:

        prediction = Prediction(
            centre_id=centre_id,
            prediction_type=prediction_type,
            predicted_value=predicted_value,
            confidence=confidence,
            prediction_time=prediction_time,
            target_time=target_time,
            model_version=model_version,
        )

        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)

        return prediction

    def get_by_id(
        self,
        prediction_id: int,
    ) -> Prediction | None:

        return (
            self.db.query(Prediction)
            .filter(Prediction.id == prediction_id)
            .first()
        )

    def create_feedback(
        self,
        prediction_id: int,
        actual_value: float,
        error: float,
    ) -> Feedback:

        feedback = Feedback(
            prediction_id=prediction_id,
            actual_value=actual_value,
            error=error,
        )

        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)

        return feedback