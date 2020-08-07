from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "devnet example api"}


def test_get_inventory():
    item = "fake_item"
    response = client.get(f"/inventory/{item}")
    assert response.status_code == 200
    assert response.json() == {"item": f"{item}"}


def test_read_main():
    body = {
        "name": "device1",
        "description": "device1 des",
        "ip": "10.1.1.1"
        }
    response = client.post("/inventory/", json=body)
    assert response.status_code == 200
    assert response.json() == {
        "created": {
            "name": "device1",
            "description": "device1 des",
            "ip": "10.1.1.1"
            }
        }
