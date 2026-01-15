from logging import getLogger

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.config import config

logger = getLogger(__name__)


class BearerAuthentication(HTTPBearer):
    """
    Аутентификация по Bearer Токену в хэдерах

    Пример хэдера:
    Authorization: Bearer {Token}
    """

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        bearer_data = await super().__call__(request)
        if bearer_data.credentials != config.BEARER_TOKEN_FOR_API:
            raise HTTPException(status_code=403, detail="Invalid token for API.")
        return
