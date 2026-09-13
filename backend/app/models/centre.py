from typing import List

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampMixin
from app.core.database import Base


class Centre(TimestampMixin, Base):
    __tablename__ = "centres"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    address: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ACTIVE",
    )

    capacity_per_hour: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=20,
    )

    operators: Mapped[List["Operator"]] = relationship(
        back_populates="centre",
    )