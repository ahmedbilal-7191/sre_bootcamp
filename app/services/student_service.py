import logging
from app.extensions import db
from app.models.student import Student
from app.utils.custom_errors import DuplicateError,NotFoundError

logger = logging.getLogger(__name__)

def create_student(student):
    existing = Student.query.filter_by(email=student.email).first()
    if existing:
        raise DuplicateError("A student with this email already exists")

    try:
        db.session.add(student)
        db.session.commit()
        logger.info(f"Student created: {student}")
        return {
            "id": student.id,
            "name": student.name,
            "email": student.email
        }
    except Exception:
        logger.exception("Failed to create student")
        db.session.rollback()
        raise

def generate_error():
    raise Exception("This is a generated error for testing purposes")
    

def get_all_students():
    students = Student.query.all()
    logger.info("Fetched all students")
    return [{"id": s.id, "name": s.name, "email": s.email} for s in students]
    
def get_student_by_id(student_id: int):
    student = Student.query.get(student_id)
    if not student:
        logger.warning(f"Student {student_id} not found")
        raise NotFoundError(f"Student with id {student_id} not found")
    return {
        "id": student.id,
        "name": student.name,
        "email": student.email
    }
    
def update_student(student_id: int, data: dict):
    student = Student.query.get(student_id)
    if not student:
        logger.warning(f"Student {student_id} not found")
        raise NotFoundError(f"Student with id {student_id} not found")

    # if updating email
    if "email" in data and data["email"] != student.email:
        if Student.query.filter_by(email=data["email"]).first():
            logger.warning(f"Duplicate email update attempt: {data['email']}")
            raise DuplicateError("Email already exists")

    try:
        for key, value in data.items():
            setattr(student, key, value)

        db.session.commit()
        logger.info(f"Student updated: {student}")
        return {
            "id": student.id,
            "name": student.name,
            "email": student.email
        }
    
    except Exception:
        logger.exception(f"Failed updating student {student_id}")
        db.session.rollback()
        raise
    
def delete_student(student_id: int):
    student = Student.query.get(student_id)
    if not student:
        logger.warning(f"Student {student_id} not found")
        raise NotFoundError(f"Student with id {student_id} not found")
    try:
        db.session.delete(student)
        db.session.commit()
        logger.info(f"Student deleted: {student_id}")
        return {"student_id": student_id}
    except Exception:
        logger.exception(f"Failed deleting student {student_id}")
        db.session.rollback()
        raise
    