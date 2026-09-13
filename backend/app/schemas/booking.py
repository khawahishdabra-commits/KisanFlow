from datetime import date, time

from pydantic import BaseModel, ConfigDict, Field


class BookingCreate(BaseModel):
    centre_id: int
    crop_id: int
    booking_date: date
    slot_time: time
    quantity: float = Field(gt=0)


class BookingResponse(BaseModel):
    id: int
    farmer_id: int
    centre_id: int
    crop_id: int
    booking_date: date
    slot_time: time
    quantity: float
    status: str

    model_config = ConfigDict(
        from_attributes=True
    )