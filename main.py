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
#добавить логирование в проект
#добавить pytest, необходимо будет написать несколько юнит-тестов для покрытия работы с бд и с роутерами