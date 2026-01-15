from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.public.services.directory import DirectoryService
from app.public.services.dependency import get_directory_service
from api.public.v1.response import (
    BuildingListResponse,
    OrganizationListResponse,
    OrganizationInRadiusListResponse,
    OrganizationInBboxListResponse,
    OrganizationByActivitySubtreeResponse,
    ActivityListResponse,
    OrganizationDetailResponse,
)
from core.fastapi.decorators.service import service_response_decorator
from core.fastapi.dependencies import BearerAuthentication


public_router = APIRouter(prefix="/directory", tags=["Directory"], dependencies=[Depends(BearerAuthentication())])


@public_router.get(
    "/buildings",
    response_model=BuildingListResponse,
    summary="Get list of buildings",
)
@service_response_decorator()
async def get_buildings(
    directory_service: Annotated[DirectoryService, Depends(get_directory_service)],
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """
    Получить список зданий
    """
    return await directory_service.get_list_buildings(limit=limit, offset=offset)


@public_router.get(
    "/organizations/search",
    response_model=OrganizationListResponse,
    summary="Search organizations by name",
)
@service_response_decorator()
async def search_organizations(
    directory_service: Annotated[DirectoryService, Depends(get_directory_service)],
    name: str = Query(..., min_length=1),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """
    Поиск организаций по имени
    """
    return await directory_service.get_organizations_by_name(name=name, limit=limit, offset=offset)


@public_router.get(
    "/organizations/radius",
    response_model=OrganizationInRadiusListResponse,
    summary="Get organizations in radius",
)
@service_response_decorator()
async def get_organizations_in_radius(
    directory_service: Annotated[DirectoryService, Depends(get_directory_service)],
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    radius_m: float = Query(..., gt=0),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """
    Получить список организаций в радиусе от точки
    """
    return await directory_service.get_organizations_in_radius(
        lat=lat,
        lon=lon,
        radius_m=radius_m,
        limit=limit,
        offset=offset,
    )


@public_router.get(
    "/organizations/bbox",
    response_model=OrganizationInBboxListResponse,
    summary="Get organizations in bounding box",
)
@service_response_decorator()
async def get_organizations_in_bbox(
    directory_service: Annotated[DirectoryService, Depends(get_directory_service)],
    min_lat: float = Query(..., ge=-90, le=90),
    min_lon: float = Query(..., ge=-180, le=180),
    max_lat: float = Query(..., ge=-90, le=90),
    max_lon: float = Query(..., ge=-180, le=180),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """
    Получить список организаций в bounding box
    """
    return await directory_service.get_organizations_in_bbox(
        min_lat=min_lat,
        min_lon=min_lon,
        max_lat=max_lat,
        max_lon=max_lon,
        limit=limit,
        offset=offset,
    )


@public_router.get(
    "/activities",
    response_model=ActivityListResponse,
    summary="Get list of activities",
)
@service_response_decorator()
async def get_activities(
    directory_service: Annotated[DirectoryService, Depends(get_directory_service)],
):
    """
    Получить список всех активностей
    """
    return await directory_service.get_list_activities()


@public_router.get(
    "/organizations/{organization_id}",
    response_model=OrganizationDetailResponse,
    summary="Get organization by ID",
)
@service_response_decorator()
async def get_organization(
    organization_id: int,
    directory_service: Annotated[DirectoryService, Depends(get_directory_service)],
):
    """
    Получить детальную информацию об организации по ID
    """
    return await directory_service.get_organization_by_id(organization_id)


@public_router.get(
    "/activities/{activity_id}/organizations/exact",
    response_model=OrganizationListResponse,
    summary="Get organizations by exact activity",
)
@service_response_decorator()
async def get_organizations_by_activity_exact(
    activity_id: int,
    directory_service: Annotated[DirectoryService, Depends(get_directory_service)],
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """
    Получить список организаций по точному совпадению деятельности
    """
    return await directory_service.get_list_organizations_by_activity_exact(
        activity_id=activity_id,
        limit=limit,
        offset=offset,
    )


@public_router.get(
    "/buildings/{building_id}/organizations",
    response_model=OrganizationListResponse,
    summary="Get organizations by building",
)
@service_response_decorator()
async def get_organizations_by_building(
    building_id: int,
    directory_service: Annotated[DirectoryService, Depends(get_directory_service)],
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """
    Получить список организаций в здании
    """
    return await directory_service.get_list_organizations_by_building(
        building_id=building_id,
        limit=limit,
        offset=offset,
    )


@public_router.get(
    "/activities/{activity_id}/organizations/subtree",
    response_model=OrganizationByActivitySubtreeResponse,
    summary="Get organizations by activity subtree",
)
@service_response_decorator()
async def get_organizations_by_activity_subtree(
    activity_id: int,
    directory_service: Annotated[DirectoryService, Depends(get_directory_service)],
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """
    Получить список организаций по поддереву активности
    """
    return await directory_service.get_organizations_by_activity_subtree(
        activity_id=activity_id,
        limit=limit,
        offset=offset,
    )
