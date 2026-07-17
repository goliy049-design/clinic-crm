from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc, context):
    """
    Wraps DRF's default exception handler to return a consistent
    error envelope across all apps: {"success": false, "errors": {...}}
    """
    response = drf_exception_handler(exc, context)

    if response is not None:
        response.data = {
            "success": False,
            "errors": response.data,
        }

    return response
