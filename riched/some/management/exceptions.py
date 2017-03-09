# -*- coding: utf-8 -*-

from django.utils import six
from django.utils.encoding import force_text

from rest_framework import status
from rest_framework.exceptions import APIException, ErrorDetail

from .status_codes import STATUS_CODES


def _get_error_details(data, default_code=None, is_unique=False):
    """
    Descend into a nested data structure, forcing any
    lazy translation strings or strings into `ErrorDetail`.
    """
    text = force_text(data)
    code = getattr(data, 'code', default_code)
    return ErrorDetail(text, code)


class ValidationErrorByCode(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'invalid'
    default_custom_code = '40000'

    def __init__(self, code):

        if code is None:
            code = self.default_custom_code

        if type(code) == int:
            code = str(code)

        message = STATUS_CODES[code]

        data = {
            'code': code,
            'message': message
        }

        self.detail = _get_error_details(data, self.default_code)

    def __str__(self):
        return six.text_type(self.detail)
