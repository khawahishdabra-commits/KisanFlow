from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampMixin
from app.core.database import Base


class Prediction(TimestampMixin, Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    centre_id: Mapped[int] = mapped_column(
        ForeignKey("centres.id"),
        nullable=False,
    )

    prediction_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    predicted_value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )

    prediction_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    target_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    model_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="rule-v1",
    )

    centre = relationship("Centre")