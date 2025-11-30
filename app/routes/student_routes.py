from flask import Blueprint, request, jsonify
from app.schemas.student_schema import StudentSchema
from app.services import student_service
from app.extensions import db
from app.utils.helpers import format_response

student_bp = Blueprint("students", __name__, url_prefix="/api/v1")

student_schema = StudentSchema()

# Healthcheck
@student_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

@student_bp.route("/error", methods=["GET"])
def error_check():
    student_service.generate_error()
    return jsonify({"status": "Error"}), 500

@student_bp.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
    student = student_schema.load(data, session=db.session)
    student_data = student_service.create_student(student)
    response = format_response(data=student_data, message="Student created")
    return jsonify(response), 201


@student_bp.route("/students", methods=["GET"])
def get_students():
    students = student_service.get_all_students()
    response = format_response(data=students, message="All students retrieved")
    return jsonify(response), 200


@student_bp.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = student_service.get_student_by_id(student_id)
    response = format_response(data=student, message="Student retrieved")
    return jsonify(response), 200



@student_bp.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json()
    student = student_service.update_student(student_id, data)
    response = format_response(data=student, message="Student updated")
    return jsonify(response), 200
  

@student_bp.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    result = student_service.delete_student(student_id)
    response = format_response(message=f"Student {result['student_id']} deleted")
    return jsonify(response), 200

