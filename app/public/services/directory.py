from dataclasses import dataclass

from api.public.v1.response import (
    OrganizationDetailResponseSchema,
    BuildingResponseSchema,
    OrganizationShortResponseSchema,
    OrganizationInRadiusResponseSchema,
    ActivityResponse,
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
        return OrganizationDetailResponseSchema(**result)

    async def get_list_buildings(self, limit: int = 10, offset: int = 0) -> list[BuildingResponseSchema]:
        """
        Получить список зданий
        """
        result = await self._directory_repository.get_list_buildings(limit=limit, offset=offset)
        result_schema = [BuildingResponseSchema(id=r.id, address=r.address, lat=r.lat, lon=r.lon) for r in result]

        return result_schema

    async def get_list_organizations_by_building(
        self,
        building_id: int,
        limit: int = 10,
        offset: int = 0,
    ) -> list[OrganizationShortResponseSchema]:
        """
        Получить список организаций по зданию
        """
        result = await self._directory_repository.get_list_organizations_by_building(
            building_id=building_id,
            limit=limit,
            offset=offset,
        )
        return [
            OrganizationShortResponseSchema(
                id=r.id,
                name=r.name,
            )
            for r in result
        ]

    async def get_list_organizations_by_activity_exact(
        self,
        activity_id: int,
        limit: int = 10,
        offset: int = 0,
    ) -> list[OrganizationShortResponseSchema]:
        """
        Получить список организаций по точному совпадению деятельности
        """
        result = await self._directory_repository.get_list_organizations_by_activity_exact(
            activity_id=activity_id,
            limit=limit,
            offset=offset,
        )
        return [
            OrganizationShortResponseSchema(
                id=r.id,
                name=r.name,
            )
            for r in result
        ]

    async def get_organizations_by_activity_subtree(
        self,
        activity_id: int,
        limit: int = 10,
        offset: int = 0,
    ) -> list[OrganizationShortResponseSchema]:
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

        return [OrganizationShortResponseSchema(id=r.id, name=r.name) for r in result]

    async def get_organizations_by_name(
        self,
        name: str,
        limit: int = 10,
        offset: int = 0,
    ) -> list[OrganizationShortResponseSchema]:
        """
        Получить список организаций по имени
        """
        result = await self._directory_repository.get_organizations_by_name(name=name, limit=limit, offset=offset)
        return [
            OrganizationShortResponseSchema(
                id=r.id,
                name=r.name,
            )
            for r in result
        ]

    async def get_organizations_in_radius(
        self,
        lat: float,
        lon: float,
        radius_m: float,
        limit: int = 10,
        offset: int = 0,
    ) -> list[OrganizationInRadiusResponseSchema]:
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
        return [
            OrganizationInRadiusResponseSchema(
                id=r.id,
                name=r.name,
                building_id=r.building_id,
                address=r.address,
                distance_m=r.distance_m,
            )
            for r in result
        ]

    async def get_organizations_in_bbox(
        self,
        min_lat: float,
        min_lon: float,
        max_lat: float,
        max_lon: float,
        limit: int = 10,
        offset: int = 0,
    ) -> list[OrganizationShortResponseSchema]:
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
        return [
            OrganizationShortResponseSchema(
                id=r.id,
                name=r.name,
            )
            for r in result
        ]

    async def get_list_activities(self) -> list[ActivityResponse]:
        """
        Получить список деятельности
        """
        result = await self._directory_repository.get_list_activities()
        return [
            ActivityResponse(
                id=r.id,
                name=r.name,
                path=str(r.path),
                parent_id=r.parent_id,
            )
            for r in result
        ]
