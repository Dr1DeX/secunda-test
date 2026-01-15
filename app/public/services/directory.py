from dataclasses import dataclass

from api.public.v1.response import (
    OrganizationDetailResponse,
    BuildingListResponse,
    OrganizationListResponse,
    OrganizationByActivitySubtreeResponse,
    OrganizationInRadiusListResponse,
    OrganizationInBboxListResponse,
    ActivityListResponse,
)
from core.exceptions.service import ServiceAPIResponseStatus, ServiceAPIException
from core.exceptions.service.enum import ServiceAPIResponseMessage
from repositories.directory import DirectoryRepository


@dataclass
class DirectoryService:
    _directory_repository: DirectoryRepository

    async def get_organization_by_id(self, organization_id: int):
        """
        Получить организацию по ID
        """
        result = await self._directory_repository.get_organization_by_id(organization_id)
        if not result:
            raise ServiceAPIException(
                status=ServiceAPIResponseStatus.NOT_FOUND_DATA,
                message=ServiceAPIResponseMessage.NOT_FOUND_DATA,
                extra_data={"organization_id": organization_id},
            )
        return OrganizationDetailResponse(**result)

    async def get_list_buildings(self, limit: int = 10, offset: int = 0) -> BuildingListResponse:
        """
        Получить список зданий
        """
        result = await self._directory_repository.get_list_buildings(limit=limit, offset=offset)
        return BuildingListResponse(**result)

    async def get_list_organizations_by_building(
        self,
        building_id: int,
        limit: int = 10,
        offset: int = 0,
    ) -> OrganizationListResponse:
        """
        Получить список организаций по зданию
        """
        result = await self._directory_repository.get_list_organizations_by_building(
            building_id=building_id,
            limit=limit,
            offset=offset,
        )
        return OrganizationListResponse(**result)

    async def get_list_organizations_by_activity_exact(
        self,
        activity_id: int,
        limit: int = 10,
        offset: int = 0,
    ) -> OrganizationListResponse:
        """
        Получить список организаций по точному совпадению деятельности
        """
        result = await self._directory_repository.get_list_organizations_by_activity_exact(
            activity_id=activity_id,
            limit=limit,
            offset=offset,
        )
        return OrganizationListResponse(**result)

    async def get_organizations_by_activity_subtree(
        self,
        activity_id: int,
        limit: int = 10,
        offset: int = 0,
    ) -> OrganizationByActivitySubtreeResponse:
        """
        Получить список организаций по поддереву деятельности
        """
        result = await self._directory_repository.get_organizations_by_activity_subtree(
            activity_id=activity_id,
            limit=limit,
            offset=offset,
        )
        if not result:
            raise ServiceAPIException(
                status=ServiceAPIResponseStatus.NOT_FOUND_DATA,
                message=ServiceAPIResponseMessage.NOT_FOUND_DATA,
                extra_data={"activity_id": activity_id},
            )
        return OrganizationByActivitySubtreeResponse(**result)

    async def get_organizations_by_name(self, name: str, limit: int = 10, offset: int = 0) -> OrganizationListResponse:
        """
        Получить список организаций по имени
        """
        result = await self._directory_repository.get_organizations_by_name(name=name, limit=limit, offset=offset)
        return OrganizationListResponse(**result)

    async def get_organizations_in_radius(
        self,
        lat: float,
        lon: float,
        radius_m: float,
        limit: int = 10,
        offset: int = 0,
    ) -> OrganizationInRadiusListResponse:
        """
        Получить список организаций в радиусе
        """
        result = await self._directory_repository.get_organizations_in_radius(
            lat=lat,
            lon=lon,
            radius_m=radius_m,
            limit=limit,
            offset=offset,
        )
        return OrganizationInRadiusListResponse(**result)

    async def get_organizations_in_bbox(
        self,
        min_lat: float,
        min_lon: float,
        max_lat: float,
        max_lon: float,
        limit: int = 10,
        offset: int = 0,
    ) -> OrganizationInBboxListResponse:
        """
        Получить список организаций в прямоугольной области
        """
        result = await self._directory_repository.get_organizations_in_bbox(
            min_lat=min_lat,
            min_lon=min_lon,
            max_lat=max_lat,
            max_lon=max_lon,
            limit=limit,
            offset=offset,
        )
        return OrganizationInBboxListResponse(**result)

    async def get_list_activities(self) -> ActivityListResponse:
        """
        Получить список деятельности
        """
        result = await self._directory_repository.get_list_activities()
        return ActivityListResponse(**result)
