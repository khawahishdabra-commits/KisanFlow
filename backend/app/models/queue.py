from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Queue(Base):
    __tablename__ = "queues"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    centre_id: Mapped[int] = mapped_column(
        ForeignKey("centres.id"),
        nullable=False,
    )

    queue_length: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    avg_service_time: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=10.0,
    )

    estimated_wait_minutes: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    centre: Mapped["Centre"] = relationship(
        "Centre",
    )