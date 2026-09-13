from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampMixin
from app.core.database import Base


class Crop(TimestampMixin, Base):
    __tablename__ = "crops"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    unit: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="quintal",
    )