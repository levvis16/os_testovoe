from datetime import date

from sqlalchemy.orm import Session

from app.schemas.booking import BookingCreate, BookingOut


def create_booking(db: Session, data: BookingCreate) -> BookingOut:
    raise NotImplementedError


def get_bookings(db: Session, booking_date: date | None = None) -> list[BookingOut]:
    raise NotImplementedError


def get_booking(db: Session, booking_id: int) -> BookingOut:
    raise NotImplementedError


def cancel_booking(db: Session, booking_id: int) -> BookingOut:
    raise NotImplementedError
