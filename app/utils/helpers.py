def format_response(data=None, message=None, status="success"):
    """
    Consistent success response format.
    """
    response = {"status": status}
    if message:
        response["message"] = message
    if data is not None:
        response["data"] = data
    return response