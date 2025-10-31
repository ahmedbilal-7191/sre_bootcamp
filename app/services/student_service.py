import logging
from app.extensions import db
from app.models.student import Student
from app.utils.helpers import format_response

logger = logging.getLogger(__name__)

def create_student(student):
    db.session.add(student)
    db.session.commit()
    logger.info(f"Student created: {student}")
    return format_response(
        data={"id": student.id, "name": student.name, "email": student.email},
        message="Student created"
    )

def get_all_students():
    students = Student.query.all()
    return format_response(
        data=[{"id": s.id, "name": s.name, "email": s.email} for s in students],
        message="All students retrieved"
    )

def get_student_by_id(student_id: int):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found")
    return format_response(
        data={"id": student.id, "name": student.name, "email": student.email},
        message="Student retrieved"
    )

def update_student(student_id: int, data: dict):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found")

    for key, value in data.items():
        setattr(student, key, value)

    db.session.commit()
    logger.info(f"Student updated: {student}")
    return format_response(
        data={"id": student.id, "name": student.name, "email": student.email},
        message="Student updated"
    )

def delete_student(student_id: int):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found")

    db.session.delete(student)
    db.session.commit()
    logger.info(f"Student deleted: {student}")
    return format_response(message=f"Student {student_id} deleted")
