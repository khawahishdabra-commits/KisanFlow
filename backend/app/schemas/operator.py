from pydantic import BaseModel
from datetime import datetime

class OperatorCentre(BaseModel):
    id: int
    name: str


class OperatorQueue(BaseModel):
    current_queue: int
    estimated_wait_minutes: float


class OperatorPredictions(BaseModel):
    eta_minutes: float
    congestion: str
    predicted_workload: float


class OperatorResource(BaseModel):
    type: str
    total: int
    available: int
    status: str


class OperatorDashboardResponse(BaseModel):
    centre: OperatorCentre
    queue: OperatorQueue
    predictions: OperatorPredictions
    resources: list[OperatorResource]

class ResourceRecommendationResponse(BaseModel):
    resource_type: str
    recommended_change: int
    reason: str


class OperatorResourceRecommendationResponse(BaseModel):
    centre_id: int
    recommendation: ResourceRecommendationResponse | None

class SimulationRequest(BaseModel):
    centre_id: int
    resource_type: str
    resource_change: int


class SimulationResponse(BaseModel):
    centre_id: int
    resource_type: str
    resource_change: int
    before_queue: int
    after_queue: int
    before_wait: float
    after_wait: float

class FeedbackRequest(BaseModel):
    prediction_id: int
    actual_value: float


class FeedbackResponse(BaseModel):
    id: int
    prediction_id: int
    actual_value: float
    error: float

    model_config = {
        "from_attributes": True
    }

class PredictionRequest(BaseModel):
    centre_id: int
    prediction_type: str
    predicted_value: float
    confidence: float | None = None
    prediction_time: datetime
    target_time: datetime
    model_version: str = "rule-v1"


class PredictionResponse(BaseModel):
    id: int
    centre_id: int
    prediction_type: str
    predicted_value: float
    confidence: float | None
    prediction_time: datetime
    target_time: datetime
    model_version: str

    model_config = {
        "from_attributes": True
    }