import pytest
from app.models.student import Student
from app.services import student_service
from app.utils.custom_errors import DuplicateError, NotFoundError
from app.extensions import db


def test_create_student_service(session):
    student = Student(name="Alice", age=10, grade="5th", email="alice@example.com")
    resp = student_service.create_student(student)

    # service returns raw dict (id, name, email)
    assert isinstance(resp, dict)
    assert "id" in resp
    assert resp["name"] == "Alice"
    assert resp["email"] == "alice@example.com"


def test_create_student_duplicate_service(session):
    s = Student(name="Bob", age=11, grade="6th", email="bob@example.com")
    session.add(s)
    session.commit()

    dup = Student(name="Bobby", age=12, grade="7th", email="bob@example.com")
    with pytest.raises(DuplicateError):
        student_service.create_student(dup)


def test_get_all_students_service(session):
    # ensure at least one student exists
    s1 = Student(name="Carl", age=12, grade="7th", email="carl@example.com")
    session.add(s1)
    session.commit()

    resp = student_service.get_all_students()
    assert isinstance(resp, list)
    # service returns list of dicts with id,name,email
    assert any(r["email"] == "carl@example.com" for r in resp)


def test_get_student_by_id_found_service(session):
    s = Student(name="Danny", age=13, grade="8th", email="danny@example.com")
    session.add(s)
    session.commit()

    resp = student_service.get_student_by_id(s.id)
    assert resp["name"] == "Danny"
    assert resp["email"] == "danny@example.com"


def test_get_student_by_id_not_found_service(session):
    with pytest.raises(NotFoundError):
        student_service.get_student_by_id(99999)


def test_update_student_service(session):
    s = Student(name="Eve", age=14, grade="9th", email="eve@example.com")
    session.add(s)
    session.commit()

    resp = student_service.update_student(s.id, {"name": "Evelyn"})
    assert resp["name"] == "Evelyn"
    assert resp["email"] == "eve@example.com"


def test_update_student_duplicate_email_service(session):
    s1 = Student(name="One", age=15, grade="10th", email="one@example.com")
    s2 = Student(name="Two", age=16, grade="11th", email="two@example.com")
    session.add_all([s1, s2])
    session.commit()

    with pytest.raises(DuplicateError):
        # try to update s2's email to s1's email
        student_service.update_student(s2.id, {"email": "one@example.com"})


def test_delete_student_service(session):
    s = Student(name="Frank", age=17, grade="12th", email="frank@example.com")
    session.add(s)
    session.commit()

    resp = student_service.delete_student(s.id)
    assert resp == {"student_id": s.id}
    # ensure deleted
    assert Student.query.get(s.id) is None


def test_delete_student_not_found_service(session):
    with pytest.raises(NotFoundError):
        student_service.delete_student(99999)

# import pytest
# from app.services import student_service
# from app.models.student import Student
# from app.utils.custom_errors import DuplicateError, NotFoundError
# from app.extensions import db

# def test_create_student(app):
#     with app.app_context():
#         student = Student(name="Alice", email="alice@example.com")
#         result = student_service.create_student(student)

#         assert "id" in result
#         assert result["name"] == "Alice"
#         assert result["email"] == "alice@example.com"


# def test_create_student_duplicate(app):
#     with app.app_context():
#         s1 = Student(name="A", email="dup@example.com")
#         db.session.add(s1)
#         db.session.commit()

#         s2 = Student(name="B", email="dup@example.com")

#         with pytest.raises(DuplicateError):
#             student_service.create_student(s2)


# def test_get_all_students(app):
#     with app.app_context():
#         s1 = Student(name="John", email="john@example.com")
#         s2 = Student(name="Jane", email="jane@example.com")
#         db.session.add_all([s1, s2])
#         db.session.commit()

#         result = student_service.get_all_students()

#         assert isinstance(result, list)
#         assert len(result) == 2
#         assert result[0]["name"] == "John"
#         assert result[1]["email"] == "jane@example.com"


# def test_get_student_by_id(app):
#     with app.app_context():
#         s = Student(name="Mark", email="mark@example.com")
#         db.session.add(s)
#         db.session.commit()

#         result = student_service.get_student_by_id(s.id)

#         assert result["name"] == "Mark"
#         assert result["email"] == "mark@example.com"


# def test_get_student_by_id_not_found(app):
#     with app.app_context():
#         with pytest.raises(NotFoundError):
#             student_service.get_student_by_id(99)


# def test_update_student(app):
#     with app.app_context():
#         s = Student(name="Old", email="old@example.com")
#         db.session.add(s)
#         db.session.commit()

#         updated = student_service.update_student(s.id, {
#             "name": "New",
#             "email": "new@example.com"
#         })

#         assert updated["name"] == "New"
#         assert updated["email"] == "new@example.com"


# def test_update_student_duplicate_email(app):
#     with app.app_context():
#         s1 = Student(name="A", email="a@example.com")
#         s2 = Student(name="B", email="b@example.com")
#         db.session.add_all([s1, s2])
#         db.session.commit()

#         with pytest.raises(DuplicateError):
#             student_service.update_student(s2.id, {"email": "a@example.com"})


# def test_delete_student(app):
#     with app.app_context():
#         s = Student(name="X", email="x@example.com")
#         db.session.add(s)
#         db.session.commit()

#         result = student_service.delete_student(s.id)

#         assert result == {"student_id": s.id}
#         assert Student.query.get(s.id) is None


# def test_delete_student_not_found(app):
#     with app.app_context():
#         with pytest.raises(NotFoundError):
#             student_service.delete_student(999)

# import pytest
# from app.models.student import Student
# from app.services import student_service

# def test_create_student(session):
#     student = Student(name="Alice", age=10, grade="5th", email="alice@example.com")
#     resp = student_service.create_student(student)
#     assert resp["status"] == "success"
#     assert resp["data"]["name"] == "Alice"

# def test_get_all_students(session):
#     s1 = Student(name="Bob", age=11, grade="6th", email="bob@example.com")
#     session.add(s1)
#     session.commit()
#     resp = student_service.get_all_students()
#     assert len(resp["data"]) == 1
#     assert resp["data"][0]["name"] == "Bob"

# def test_get_student_by_id_found(session):
#     s = Student(name="Charlie", age=12, grade="7th", email="charlie@example.com")
#     session.add(s)
#     session.commit()
#     resp = student_service.get_student_by_id(s.id)
#     assert resp["data"]["name"] == "Charlie"

# def test_get_student_by_id_not_found(session):
#     with pytest.raises(ValueError):
#         student_service.get_student_by_id(999)

# def test_update_student(session):
#     s = Student(name="Dave", age=13, grade="8th", email="dave@example.com")
#     session.add(s)
#     session.commit()
#     resp = student_service.update_student(s.id, {"name": "David"})
#     assert resp["data"]["name"] == "David"

# def test_delete_student(session):
#     s = Student(name="Eve", age=14, grade="9th", email="eve@example.com")
#     session.add(s)
#     session.commit()
#     resp = student_service.delete_student(s.id)
#     assert "deleted" in resp["message"]
