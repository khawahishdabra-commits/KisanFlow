from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


if TYPE_CHECKING:
    from app.models.centre import Centre


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    centre_id: Mapped[int] = mapped_column(
        ForeignKey("centres.id"),
        nullable=False,
    )

    resource_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    total_units: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    available_units: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="AVAILABLE",
    )

    centre: Mapped["Centre"] = relationship(
        "Centre",
    )