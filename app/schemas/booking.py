from datetime import date, time, timedelta
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BookingCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    phone: str = Field(pattern=r"^\+7\d{10}$")
    booking_date: date
    booking_time: time
    guests: int = Field(ge=1, le=10)

    @field_validator("booking_date")
    @classmethod
    def validate_booking_date(cls, v: date) -> date:
        today = date.today()
        max_date = today + timedelta(days=30)
        if v < today:
            raise ValueError("Booking date cannot be in the past")
        if v > max_date:
            raise ValueError("Booking date cannot be more than 30 days in the future")
        return v

    @field_validator("booking_time")
    @classmethod
    def validate_booking_time(cls, v: time) -> time:
        if v.minute != 0 or v.second != 0 or v.microsecond != 0:
            raise ValueError("Booking time must be on the hour (e.g., 12:00, 13:00)")
        if v.hour < 12 or v.hour > 22:
            raise ValueError("Booking time must be between 12:00 and 22:00")
        return v


class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str
    booking_date: date
    booking_time: time
    guests: int
    status: Literal["active", "cancelled"]
