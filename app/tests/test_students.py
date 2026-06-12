def test_create_student(client):
    payload = {"reg_no": "2312259", "name": "Shayan Muhammad Faisal", "email": "shayan@example.com"}
    response = client.post("/students", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["reg_no"] == "2312259"
    assert data["name"] == "Shayan Muhammad Faisal"
    assert "id" in data


def test_get_all_students_empty(client):
    response = client.get("/students")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_students_after_create(client):
    client.post("/students", json={
        "reg_no": "2312259",
        "name": "Shayan Muhammad Faisal",
        "email": "shayan@example.com"
    })
    response = client.get("/students")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_student_by_reg_no(client):
    client.post("/students", json={
        "reg_no": "2312259",
        "name": "Shayan Muhammad Faisal",
        "email": "shayan@example.com"
    })
    response = client.get("/students/2312259")
    assert response.status_code == 200
    assert response.json()["reg_no"] == "2312259"


def test_get_student_not_found(client):
    response = client.get("/students/9999999")
    assert response.status_code == 404


def test_duplicate_student_returns_400(client):
    payload = {"reg_no": "2312259", "name": "Shayan Muhammad Faisal", "email": "shayan@example.com"}
    client.post("/students", json=payload)
    response = client.post("/students", json=payload)
    assert response.status_code == 400
