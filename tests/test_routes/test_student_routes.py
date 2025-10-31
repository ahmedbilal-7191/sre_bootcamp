def test_health_check(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "ok"

def test_add_and_get_student(client):
    payload = {"name": "Alice", "age": 10, "grade": "5th", "email": "alice@example.com"}
    res = client.post("/api/v1/students", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    student_id = data["data"]["id"]

    # Fetch
    res = client.get(f"/api/v1/students/{student_id}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["data"]["name"] == "Alice"

def test_update_student(client):
    payload = {"name": "Bob", "age": 11, "grade": "6th", "email": "bob@example.com"}
    res = client.post("/api/v1/students", json=payload)
    student_id = res.get_json()["data"]["id"]

    update = {"name": "Bobby"}
    res = client.put(f"/api/v1/students/{student_id}", json=update)
    assert res.status_code == 200
    assert res.get_json()["data"]["name"] == "Bobby"

def test_delete_student(client):
    payload = {"name": "Charlie", "age": 12, "grade": "7th", "email": "charlie@example.com"}
    res = client.post("/api/v1/students", json=payload)
    student_id = res.get_json()["data"]["id"]

    res = client.delete(f"/api/v1/students/{student_id}")
    assert res.status_code == 200
    assert "deleted" in res.get_json()["message"]
