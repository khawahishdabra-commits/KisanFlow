from pydantic import BaseModel


class QueueIntelligence(BaseModel):

    queue_length: int

    avg_service_time: float

    estimated_wait_minutes: float


class PredictionIntelligence(BaseModel):

    eta_minutes: float

    congestion_level: str

    predicted_workload: float


class ResourceIntelligence(BaseModel):

    resource_type: str

    total_units: int

    available_units: int

    status: str


class CentreIntelligenceResponse(BaseModel):

    centre_id: int

    centre_name: str

    status: str

    queue: QueueIntelligence

    predictions: PredictionIntelligence

    resources: list[ResourceIntelligence]