from datetime import date, time
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class BookingCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    phone: str = Field(pattern=r"^\+7\d{10}$")
    booking_date: date
    booking_time: time
    guests: int = Field(ge=1, le=10)


class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str
    booking_date: date
    booking_time: time
    guests: int
    status: Literal["active", "cancelled"]
