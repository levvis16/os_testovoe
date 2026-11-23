from datetime import date, time, timedelta
from fastapi.testclient import TestClient
import pytest

from main import app
from app.database.database import Base, engine, SessionLocal
from app.models.booking import Booking


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db_session):
    from app.database.database import get_db

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_create_booking_success(client):
    """Успешное создание брони возвращает 201 и бронь со status=active."""
    tomorrow = date.today() + timedelta(days=1)
    response = client.post(
        "/bookings",
        json={
            "name": "Иван Иванов",
            "phone": "+79001234567",
            "booking_date": tomorrow.isoformat(),
            "booking_time": "12:00:00",
            "guests": 2,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Иван Иванов"
    assert data["status"] == "active"
    assert "id" in data


def test_create_booking_duplicate_slot_returns_409(client):
    """Повторная бронь на занятый слот возвращает 409."""
    tomorrow = date.today() + timedelta(days=1)
    payload = {
        "name": "Иван Иванов",
        "phone": "+79001234567",
        "booking_date": tomorrow.isoformat(),
        "booking_time": "12:00:00",
        "guests": 2,
    }
    response1 = client.post("/bookings", json=payload)
    assert response1.status_code == 201

    response2 = client.post("/bookings", json=payload)
    assert response2.status_code == 409
    assert response2.json()["detail"] == "Slot is already booked"


def test_cancel_booking_frees_slot(client):
    """Отмена брони освобождает слот для новой брони."""
    tomorrow = date.today() + timedelta(days=1)
    payload = {
        "name": "Иван Иванов",
        "phone": "+79001234567",
        "booking_date": tomorrow.isoformat(),
        "booking_time": "12:00:00",
        "guests": 2,
    }
    create_resp = client.post("/bookings", json=payload)
    booking_id = create_resp.json()["id"]

    # Отменяем
    cancel_resp = client.delete(f"/bookings/{booking_id}")
    assert cancel_resp.status_code == 200
    assert cancel_resp.json()["status"] == "cancelled"

    # Слот свободен — можно заново забронировать
    response2 = client.post("/bookings", json=payload)
    assert response2.status_code == 201