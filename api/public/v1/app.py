from fastapi import FastAPI

from api.base.v1.response.base import BaseResponseModel
from api.public.v1.router import public_router
from core.exceptions.service import ServiceAPIException
from core.exceptions.service.exceptions import Custom403Exception
from core.fastapi.exceptions.handlers import service_api_exception_handler, exception_403_handler


public_subapi = FastAPI()

public_subapi.include_router(
    public_router,
    responses={
        "default": {
            "model": BaseResponseModel,
        },
    },
)

public_subapi.add_exception_handler(ServiceAPIException, service_api_exception_handler)
public_subapi.add_exception_handler(Custom403Exception, exception_403_handler)
