from datetime import date, time

from sqlalchemy import Date, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Booking(Base):
    """Таблица броней."""

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(12))
    booking_date: Mapped[date] = mapped_column(Date)
    booking_time: Mapped[time] = mapped_column(Time)
    guests: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(9), default="active", server_default="active")
