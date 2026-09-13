from pydantic import BaseModel, ConfigDict


class CentreResponse(BaseModel):
    id: int
    name: str
    address: str
    latitude: float | None
    longitude: float | None
    status: str
    capacity_per_hour: int

    model_config = ConfigDict(
        from_attributes=True
    )