from pydantic import BaseModel, Field


class FarmerUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    language: str | None = Field(
        default=None,
        max_length=10,
    )

    latitude: float | None = None

    longitude: float | None = None