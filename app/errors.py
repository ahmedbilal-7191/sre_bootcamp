import logging
from flask import jsonify
from marshmallow import ValidationError
from app.utils.error_helpers import format_error_response
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.utils.custom_errors import DuplicateError,NotFoundError
logger = logging.getLogger(__name__)

def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        logger.warning(f"Validation error: {err.messages}")
        return jsonify(format_error_response("Validation error", details=err.messages)), 400

    # @app.errorhandler(ValueError)
    # def handle_value_error(err):
    #     logger.error(str(err))
    #     return jsonify(format_error_response(str(err))), 400
    
    @app.errorhandler(DuplicateError)
    def handle_duplicate(err):
        logger.info(str(err))
        return jsonify(format_error_response(str(err))), 409

    @app.errorhandler(NotFoundError)
    def handle_not_found(err):
        logger.info(str(err))
        return jsonify(format_error_response(str(err))), 404
    
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(err):
        logger.error("Database integrity error", exc_info=True)
        return jsonify(format_error_response("Database integrity error")), 400

    # Handles other SQL errors
    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(err):
        logger.error("Database error", exc_info=True)
        return jsonify(format_error_response("Database error")), 500


    @app.errorhandler(404)
    def handle_not_found_http(err):
        logger.warning("Unknown route")
        return jsonify(format_error_response("Resource not found")), 404

    @app.errorhandler(500)
    def handle_internal_error(err):
        logger.exception("Internal server error")
        return jsonify(format_error_response("Internal server error")), 500