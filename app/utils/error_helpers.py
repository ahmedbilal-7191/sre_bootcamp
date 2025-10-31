def format_error_response(message: str, details: dict = None):
    """
    Format error responses consistently across the API.
    """
    response = {
        "status": "error",
        "message": message
    }
    if details:
        response["details"] = details
    return response
