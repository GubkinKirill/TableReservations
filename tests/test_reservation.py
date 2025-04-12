import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_reservation():
    table = {"name": "T1", "seats": 4, "location": "терраса"}
    res = client.post("/tables/", json=table)
    table_id = res.json()["id"]

    reservation = {
        "customer_name": "Иван",
        "table_id": table_id,
        "reservation_time": "2025-04-10T18:00:00",
        "duration_minutes": 60
    }

    res = client.post("/reservations/", json=reservation)
    assert res.status_code == 200
    data = res.json()
    assert data["customer_name"] == "Иван"
    assert data["table_id"] == table_id


def test_conflict_reservation():
    table_id = client.post("/tables/", json={
        "name": "T2", "seats": 2, "location": "угол"
    }).json()["id"]

    res1 = {
        "customer_name": "Петя",
        "table_id": table_id,
        "reservation_time": "2025-04-10T18:00:00",
        "duration_minutes": 60
    }
    client.post("/reservations/", json=res1)

    res2 = {
        "customer_name": "Маша",
        "table_id": table_id,
        "reservation_time": "2025-04-10T18:30:00",
        "duration_minutes": 60
    }
    conflict = client.post("/reservations/", json=res2)
    assert conflict.status_code == 409
    assert "Table is already reserved" in conflict.json()["detail"]


def test_delete_reservation():
    table_id = client.post("/tables/", json={
        "name": "T3", "seats": 2, "location": "зал"
    }).json()["id"]

    reservation = {
        "customer_name": "Алексей",
        "table_id": table_id,
        "reservation_time": "2025-04-10T20:00:00",
        "duration_minutes": 30
    }
    res = client.post("/reservations/", json=reservation)
    res_id = res.json()["id"]

    del_res = client.delete(f"/reservations/{res_id}")
    assert del_res.status_code == 200

    get_res = client.get("/reservations/")
    assert get_res.status_code == 200
    assert all(r["id"] != res_id for r in get_res.json())