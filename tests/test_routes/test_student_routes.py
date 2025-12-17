import pytest
from app.models.student import Student


def test_health_check_route(client):
    res = client.get("/healthcheck")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "ok"


def test_add_and_get_student_route(client):
    payload = {"name": "Alice", "age": 10, "grade": "5th", "email": "alice@example.com"}
    res = client.post("/api/v1/students", json=payload)
    assert res.status_code == 201

    data = res.get_json()
    # route wraps using format_response
    assert data["status"] == "success"
    assert data["message"] == "Student created"
    assert "data" in data
    student_id = data["data"]["id"]

    # Fetch
    res = client.get(f"/api/v1/students/{student_id}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "success"
    assert data["data"]["name"] == "Alice"


def test_get_student_not_found_route(client):
    res = client.get("/api/v1/students/999999")
    assert res.status_code == 404
    data = res.get_json()
    assert data["status"] == "error"
    assert "not found" in data["message"].lower()


def test_update_student_route(client):
    payload = {"name": "Bob", "age": 11, "grade": "6th", "email": "bob@example.com"}
    res = client.post("/api/v1/students", json=payload)
    student_id = res.get_json()["data"]["id"]

    update = {"name": "Bobby"}
    res = client.put(f"/api/v1/students/{student_id}", json=update)
    assert res.status_code == 200
    json = res.get_json()
    assert json["status"] == "success"
    assert json["data"]["name"] == "Bobby"


def test_delete_student_route(client):
    payload = {"name": "Charlie", "age": 12, "grade": "7th", "email": "charlie@example.com"}
    res = client.post("/api/v1/students", json=payload)
    student_id = res.get_json()["data"]["id"]

    res = client.delete(f"/api/v1/students/{student_id}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "success"
    assert data["message"] == f"Student {student_id} deleted"


def test_validation_error_route(client):
    # Missing required fields (age, grade) -> marshmallow ValidationError -> 400
    payload = {"name": "X"}  # missing age, grade, email
    res = client.post("/api/v1/students", json=payload)
    assert res.status_code == 400
    data = res.get_json()
    assert data["status"] == "error"
    assert "validation" in data["message"].lower() or "missing" in str(data.get("details", "")).lower()

# def test_route_add_student(client):
#     payload = {"name": "Alice", "email": "alice@example.com"}
#     resp = client.post("/api/v1/students", json=payload)

#     assert resp.status_code == 201
#     json = resp.get_json()

#     assert json["status"] == "success"
#     assert json["message"] == "Student created"
#     assert json["data"]["name"] == "Alice"


# def test_route_get_students(client):
#     client.post("/api/v1/students", json={"name": "A", "email": "a@test.com"})
#     client.post("/api/v1/students", json={"name": "B", "email": "b@test.com"})

#     resp = client.get("/api/v1/students")
#     data = resp.get_json()

#     assert resp.status_code == 200
#     assert data["status"] == "success"
#     assert data["message"] == "All students retrieved"
#     assert len(data["data"]) == 2


# def test_route_get_single_student(client):
#     create = client.post("/api/v1/students", json={"name": "X", "email": "x@test.com"})
#     id = create.get_json()["data"]["id"]

#     resp = client.get(f"/api/v1/students/{id}")
#     json = resp.get_json()

#     assert resp.status_code == 200
#     assert json["message"] == "Student retrieved"
#     assert json["data"]["name"] == "X"


# def test_route_update_student(client):
#     create = client.post("/api/v1/students", json={"name": "Old", "email": "old@test.com"})
#     id = create.get_json()["data"]["id"]

#     resp = client.put(f"/api/v1/students/{id}", json={"name": "New"})
#     json = resp.get_json()

#     assert json["status"] == "success"
#     assert json["message"] == "Student updated"
#     assert json["data"]["name"] == "New"


# def test_route_delete_student(client):
#     create = client.post("/api/v1/students", json={"name": "P", "email": "p@test.com"})
#     id = create.get_json()["data"]["id"]

#     resp = client.delete(f"/api/v1/students/{id}")
#     json = resp.get_json()

#     assert json["status"] == "success"
#     assert json["message"] == f"Student {id} deleted"

# def test_health_check(client):
#     res = client.get("/api/v1/health")
#     assert res.status_code == 200
#     data = res.get_json()
#     assert data["status"] == "ok"

# def test_add_and_get_student(client):
#     payload = {"name": "Alice", "age": 10, "grade": "5th", "email": "alice@example.com"}
#     res = client.post("/api/v1/students", json=payload)
#     assert res.status_code == 201
#     data = res.get_json()
#     student_id = data["data"]["id"]

#     # Fetch
#     res = client.get(f"/api/v1/students/{student_id}")
#     assert res.status_code == 200
#     data = res.get_json()
#     assert data["data"]["name"] == "Alice"

# def test_update_student(client):
#     payload = {"name": "Bob", "age": 11, "grade": "6th", "email": "bob@example.com"}
#     res = client.post("/api/v1/students", json=payload)
#     student_id = res.get_json()["data"]["id"]

#     update = {"name": "Bobby"}
#     res = client.put(f"/api/v1/students/{student_id}", json=update)
#     assert res.status_code == 200
#     assert res.get_json()["data"]["name"] == "Bobby"

# def test_delete_student(client):
#     payload = {"name": "Charlie", "age": 12, "grade": "7th", "email": "charlie@example.com"}
#     res = client.post("/api/v1/students", json=payload)
#     student_id = res.get_json()["data"]["id"]

#     res = client.delete(f"/api/v1/students/{student_id}")
#     assert res.status_code == 200
#     assert "deleted" in res.get_json()["message"]
