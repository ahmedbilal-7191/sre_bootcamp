from flask import Blueprint, request, jsonify
from app.schemas.student_schema import StudentSchema
from app.services import student_service
from app.extensions import db

student_bp = Blueprint("students", __name__, url_prefix="/api/v1")

student_schema = StudentSchema()

# Healthcheck
@student_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

@student_bp.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
    student = student_schema.load(data, session=db.session)
    response = student_service.create_student(student)
    return jsonify(response), 201

@student_bp.route("/students", methods=["GET"])
def get_students():
    response = student_service.get_all_students()
    return jsonify(response), 200

@student_bp.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    response = student_service.get_student_by_id(student_id)
    return jsonify(response), 200

@student_bp.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json()
    response = student_service.update_student(student_id, data)
    return jsonify(response), 200

@student_bp.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    response = student_service.delete_student(student_id)
    return jsonify(response), 200
