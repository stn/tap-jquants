class JquantsError(Exception):
    pass


def raise_for_error(response):
    """Forming a response message for raising custom exception"""
    try:
        response_json = response.json()
    except Exception:
        response_json = {}

    error_code = response.status_code
    error_message = response_json.get("message", "")

    message = f"HTTP-error-code: {error_code}, Error: {error_message}"
    raise JquantsError(message) from None
