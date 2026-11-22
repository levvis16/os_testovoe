from fastapi.testclient import TestClient

def test_get_item_success(booking: TestClient):
    responce = booking.get("/bookings/1")
    assert responce.status_code == 200
    assert responce.json() == {"id":1, "name":"lev", "phone":"79092860144","booking_date": 2026_11_12, "booking_time": 12.15, "guests": 5, "status": "active"}
    pass