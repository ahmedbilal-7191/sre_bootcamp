import pytest
from app.models.student import Student
from app.services import student_service

def test_create_student(session):
    student = Student(name="Alice", age=10, grade="5th", email="alice@example.com")
    resp = student_service.create_student(student)
    assert resp["status"] == "success"
    assert resp["data"]["name"] == "Alice"

def test_get_all_students(session):
    s1 = Student(name="Bob", age=11, grade="6th", email="bob@example.com")
    session.add(s1)
    session.commit()
    resp = student_service.get_all_students()
    assert len(resp["data"]) == 1
    assert resp["data"][0]["name"] == "Bob"

def test_get_student_by_id_found(session):
    s = Student(name="Charlie", age=12, grade="7th", email="charlie@example.com")
    session.add(s)
    session.commit()
    resp = student_service.get_student_by_id(s.id)
    assert resp["data"]["name"] == "Charlie"

def test_get_student_by_id_not_found(session):
    with pytest.raises(ValueError):
        student_service.get_student_by_id(999)

def test_update_student(session):
    s = Student(name="Dave", age=13, grade="8th", email="dave@example.com")
    session.add(s)
    session.commit()
    resp = student_service.update_student(s.id, {"name": "David"})
    assert resp["data"]["name"] == "David"

def test_delete_student(session):
    s = Student(name="Eve", age=14, grade="9th", email="eve@example.com")
    session.add(s)
    session.commit()
    resp = student_service.delete_student(s.id)
    assert "deleted" in resp["message"]
