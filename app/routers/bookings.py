from datetime import date
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.booking import BookingCreate, BookingOut
from app.services import booking as booking_service

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking(data: BookingCreate, db: Session = Depends(get_db)) -> BookingOut:
    """Создать бронь. Возвращает 201 и созданную бронь со status=active."""
    return booking_service.create_booking(db, data)


@router.get("", response_model=list[BookingOut])
def get_bookings(
    booking_date: date | None = Query(default=None, alias="date"),
    db: Session = Depends(get_db),
) -> list[BookingOut]:
    """Список броней. Необязательный фильтр по дате: ?date=2026-12-15."""
    return booking_service.get_bookings(db, booking_date)


@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(booking_id: int, db: Session = Depends(get_db)) -> BookingOut:
    """Получить бронь по id. 404, если не найдена."""
    return booking_service.get_booking(db, booking_id)


@router.delete("/{booking_id}", response_model=BookingOut)
def cancel_booking(booking_id: int, db: Session = Depends(get_db)) -> BookingOut:
    """Отменить бронь: статус меняется на cancelled, запись не удаляется. Возвращает 200 и бронь."""
    return booking_service.cancel_booking(db, booking_id)
