from typing import Any

from fastapi import HTTPException
from starlette import status

from .enum import ServiceAPIResponseMessage, ServiceAPIResponseStatus


class ServiceAPIException(Exception):
    def __init__(
        self,
        status: int = ServiceAPIResponseStatus.GENERAL_ERROR,
        message: str = ServiceAPIResponseMessage.GENERAL_ERROR,
        extra_data=None,
    ):
        if extra_data is None:
            extra_data = dict()

        self.status = status
        self.message = message
        self.extra_data = extra_data


class Custom403Exception(HTTPException):
    def __init__(self, status_code: int = status.HTTP_403_FORBIDDEN, detail: Any = None, headers: dict = None) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)
