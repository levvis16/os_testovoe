from datetime import date

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from models.booking import Booking
from app.database.database import get_db
from app.schemas.booking import BookingCreate, BookingOut
from app.services import booking as booking_service

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/bookings", response_model=BookingOut, status_code=201)
async def create_booking(data: BookingCreate, db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code= status.HTTP)
    return booking_service.create_booking(db, data)


@router.get("/bookings/{booking_id}", response_model=list[BookingOut])
async def get_bookings(
    booking_date: date | None = Query(default=None, alias="date"),
    db: Session = Depends(get_db),
):
    booking_list = await db.execute(select(Booking).options(selectinload(Booking.booking_date)))
    return booking_service.get_bookings(db, booking_date)


@router.get("/bookings/{booking_id}", response_model=BookingOut)
async def get_booking(booking_id: int, db: Session = Depends(get_db)):
    user = await db.get(Booking, booking_id)
    if not user:
        raise HTTPException(status_code=404, detail="booking not found")
    return booking_service.get_booking(db, booking_id)


@router.delete("/bookings/{booking_id}", response_model=BookingOut)
async def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    user_to_change = await db.get(Booking, booking_id)
    if not user_to_change:
        raise HTTPException(status_code=404, detail="booking not found")
    user_to_change.status = 'cancelled'

    db.add(user_to_change)
    db.refresh()
    db.commit(user_to_change)

    return user_to_change
