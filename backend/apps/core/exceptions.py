"""
Custom exception handlers for the API.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the response format
        custom_response_data = {
            'success': False,
            'error': {
                'message': str(exc),
                'details': response.data if isinstance(response.data, dict) else {'detail': response.data}
            }
        }
        response.data = custom_response_data

    return response


class PaymentError(Exception):
    """Custom exception for payment-related errors."""
    pass


class VerificationError(Exception):
    """Custom exception for verification-related errors."""
    pass


class WithdrawalError(Exception):
    """Custom exception for withdrawal-related errors."""
    pass

