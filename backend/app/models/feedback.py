from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampMixin
from app.core.database import Base


class Feedback(TimestampMixin, Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    prediction_id: Mapped[int] = mapped_column(
        ForeignKey("predictions.id"),
        nullable=False,
    )

    actual_value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    error: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    prediction = relationship("Prediction")