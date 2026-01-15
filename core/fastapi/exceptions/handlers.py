from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import ORJSONResponse

from api.base.v1.response import BaseResponseModel
from core.exceptions.service import ServiceAPIException

app = FastAPI()


@app.exception_handler(ServiceAPIException)
async def service_api_exception_handler(request: Request, exc: ServiceAPIException):
    body = BaseResponseModel(
        result=exc.extra_data or {},
        status=exc.status,
        error_message=exc.message,
    )
    return ORJSONResponse(
        content=body.model_dump(),
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@app.exception_handler(HTTPException)
async def exception_403_handler(request: Request, exc: HTTPException):
    return ORJSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=exc.detail,
    )
