import logging

from django.http import JsonResponse, Http404
from rest_framework import status
from rest_framework.views import exception_handler

_logger = logging.getLogger(__name__)


def _not_found_handler(exc, context):
    _logger.warning(f"Not Found.\nexc: {exc.__class__}, {exc}\ncontext: {context}")
    return JsonResponse({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


def _server_error_handler(exc, context):
    _logger.error(f"Internal Server Error.\nexc: {exc.__class__}, {exc}\ncontext: {context}")
    return JsonResponse({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def global_exception_handler(exc, context):
    if isinstance(exc, Http404):
        return _not_found_handler(exc, context)

    response = exception_handler(exc, context)

    if response is None:
        return _server_error_handler(exc, context)

    _logger.error(f'Not Defined Error.\nexc: {exc.__class__}, {exc}\ncontext: {context}')
    return response
