from pydantic import BaseModel, Field


class LocationInput(BaseModel):
    lat: float
    lon: float


class RecommendationRequest(BaseModel):
    crop_id: int
    quantity: float = Field(gt=0)
    location: LocationInput


class RecommendedCentre(BaseModel):
    id: int
    name: str
    score: float
    expected_net_return: float
    price: float
    eta_minutes: float
    congestion: str
    distance_km: float
    reason: str


class CentreAlternative(BaseModel):
    id: int
    name: str
    score: float
    expected_net_return: float
    price: float
    eta_minutes: float
    congestion: str
    distance_km: float


class RecommendationResponse(BaseModel):
    recommended_centre: RecommendedCentre
    alternatives: list[CentreAlternative]