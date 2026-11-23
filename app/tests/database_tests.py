from datetime import date, time, timedelta
import pytest

from app.database.database import Base, engine, SessionLocal
from app.schemas.booking import BookingCreate
from app.services import booking as booking_service


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_booking_service(db_session):
    """Сервис создает бронь и возвращает BookingOut."""
    tomorrow = date.today() + timedelta(days=1)
    data = BookingCreate(
        name="Иван Иванов",
        phone="+79001234567",
        booking_date=tomorrow,
        booking_time=time(12, 0),
        guests=2,
    )
    result = booking_service.create_booking(db_session, data)
    assert result.id == 1
    assert result.name == "Иван Иванов"
    assert result.status == "active"


def test_duplicate_slot_raises_409(db_session):
    """Сервис выбрасывает 409 при попытке забронировать занятый слот."""
    tomorrow = date.today() + timedelta(days=1)
    data = BookingCreate(
        name="Иван Иванов",
        phone="+79001234567",
        booking_date=tomorrow,
        booking_time=time(12, 0),
        guests=2,
    )
    booking_service.create_booking(db_session, data)

    data2 = BookingCreate(
        name="Петр Петров",
        phone="+79001234568",
        booking_date=tomorrow,
        booking_time=time(12, 0),
        guests=3,
    )
    with pytest.raises(Exception) as exc_info:
        booking_service.create_booking(db_session, data2)
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Slot is already booked"


def test_cancelled_booking_frees_slot(db_session):
    """Отмененная бронь освобождает слот для новой брони."""
    tomorrow = date.today() + timedelta(days=1)
    data = BookingCreate(
        name="Иван Иванов",
        phone="+79001234567",
        booking_date=tomorrow,
        booking_time=time(12, 0),
        guests=2,
    )
    booking = booking_service.create_booking(db_session, data)
    booking_id = booking.id

    cancelled = booking_service.cancel_booking(db_session, booking_id)
    assert cancelled.status == "cancelled"

    data2 = BookingCreate(
        name="Петр Петров",
        phone="+79001234568",
        booking_date=tomorrow,
        booking_time=time(12, 0),
        guests=3,
    )
    new_booking = booking_service.create_booking(db_session, data2)
    assert new_booking.id != booking_id
    assert new_booking.status == "active"