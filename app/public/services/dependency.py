from fastapi import Depends

from app.public.services.directory import DirectoryService
from repositories.dependency import get_directory_repository
from repositories.directory import DirectoryRepository


async def get_directory_service(
    directory_repository: DirectoryRepository = Depends(get_directory_repository),
) -> DirectoryService:
    return DirectoryService(_directory_repository=directory_repository)
