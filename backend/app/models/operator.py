from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampMixin
from app.core.database import Base


if TYPE_CHECKING:
    from app.models.centre import Centre


class Operator(TimestampMixin, Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    centre_id: Mapped[int] = mapped_column(
        ForeignKey("centres.id"),
        nullable=False,
    )

    centre: Mapped["Centre"] = relationship(
        back_populates="operators",
    )