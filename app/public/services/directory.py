from dataclasses import dataclass

from repositories.directory import DirectoryRepository


@dataclass
class DirectoryService:
    _directory_repository: DirectoryRepository

    ...
