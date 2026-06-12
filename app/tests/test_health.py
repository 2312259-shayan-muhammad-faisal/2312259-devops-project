def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_contains_status_ok(client):
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "ok"


def test_health_contains_registration_number(client):
    response = client.get("/health")
    data = response.json()
    assert data["student"] == "2312259"


def test_health_contains_db_field(client):
    response = client.get("/health")
    data = response.json()
    assert "db" in data
