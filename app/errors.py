import logging
from flask import jsonify
from marshmallow import ValidationError
from app.utils.error_helpers import format_error_response

logger = logging.getLogger(__name__)

def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        logger.error(f"Validation error: {err.messages}")
        return jsonify(format_error_response("Validation error", details=err.messages)), 400

    @app.errorhandler(ValueError)
    def handle_value_error(err):
        logger.error(str(err))
        return jsonify(format_error_response(str(err))), 404

    @app.errorhandler(404)
    def handle_not_found(err):
        logger.warning("Resource not found")
        return jsonify(format_error_response("Resource not found")), 404

    @app.errorhandler(500)
    def handle_internal_error(err):
        logger.exception("Internal server error")
        return jsonify(format_error_response("Internal server error")), 500
