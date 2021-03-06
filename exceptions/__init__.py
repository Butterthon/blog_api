# /usr/bin/env python
# -*- coding: utf-8 -*-
import traceback

from fastapi import status, HTTPException

from exceptions.error_message import ErrorMessage


class ApiException(HTTPException):
    """ API例外
    """
    default_status_code = status.HTTP_400_BAD_REQUEST

    def __init__(
        self,
        *errors,
        status_code: int = default_status_code
    ) -> None:
        self.status_code = status_code
        self.detail = [
            {
                'error_code': str(error['error_code']),
                'error_msg': error['error_code'].message.format(*error['msg_params']),
            } for error in list(errors)
        ]
        super().__init__(self.status_code, self.detail)


class SystemException(HTTPException):
    """ システム例外
    """
    def __init__(self, e: Exception) -> None:
        self.exc = e
        self.stack_trace = traceback.format_exc()
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = [
            {
                'error_code': str(ErrorMessage.INTERNAL_SERVER_ERROR()),
                'error_msg': ErrorMessage.INTERNAL_SERVER_ERROR.message
            }
        ]
        super().__init__(self.status_code, self.detail)


def create_error(error_code: ErrorMessage, *msg_params) -> dict:
    """ エラー生成

    Examples
    --------
    >>> create_error(messages.INTERNAL_SERVER_ERROR)
    {'error_code': INTERNAL_SERVER_ERROR, 'msg_params': None}

    >>> create_error(messages.E_REGISTRATION, 'ユーザー')
    {'error_code': E_REGISTRATION, 'msg_params': ユーザー}
    """
    return {
        'error_code': error_code(),
        'msg_params': msg_params,
    }
