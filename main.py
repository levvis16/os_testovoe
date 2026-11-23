from fastapi import FastAPI

from app.database.database import Base, engine
from app.models.booking import Booking
from app.routers.bookings import router as bookings_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Сервис бронирования столика",
    version="0.1.0",
)

app.include_router(bookings_router)


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "ok"}