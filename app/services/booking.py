from datetime import date
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingOut
from fastapi import HTTPException, status


def create_booking(db: Session, data: BookingCreate) -> BookingOut:
    """Создать новую бронь. Проверяет уникальность слота."""
    booking = Booking(
        name=data.name,
        phone=data.phone,
        booking_date=data.booking_date,
        booking_time=data.booking_time,
        guests=data.guests,
        status="active",
    )
    db.add(booking)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Slot is already booked",
        )
    db.refresh(booking)
    return BookingOut.model_validate(booking)


def get_bookings(db: Session, booking_date: date | None = None) -> list[BookingOut]:
    """Получить список броней с опциональным фильтром по дате."""
    stmt = select(Booking)
    if booking_date:
        stmt = stmt.where(Booking.booking_date == booking_date)
    stmt = stmt.order_by(Booking.booking_date, Booking.booking_time)
    bookings = db.execute(stmt).scalars().all()
    return [BookingOut.model_validate(b) for b in bookings]


def get_booking(db: Session, booking_id: int) -> BookingOut:
    """Получить бронь по ID. 404 если не найдена."""
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )
    return BookingOut.model_validate(booking)


def cancel_booking(db: Session, booking_id: int) -> BookingOut:
    """Отменить бронь: меняет статус на cancelled. 404 если не найдена."""
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )
    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)
    return BookingOut.model_validate(booking)
