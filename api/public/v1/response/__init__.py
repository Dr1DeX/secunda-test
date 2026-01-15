from pydantic import BaseModel

from api.base.v1.response import BaseResponseModel


class BuildingResponseSchema(BaseModel):
    id: int | None = None
    address: str | None = None
    lat: float | None = None
    lon: float | None = None


class BuildingListResponse(BaseResponseModel):
    result: list[BuildingResponseSchema]


class OrganizationShortResponseSchema(BaseModel):
    id: int
    name: str


class OrganizationPhoneResponse(BaseModel):
    phone: str


class OrganizationActivityResponseSchema(BaseModel):
    id: int
    name: str
    path: str
    level: int | None = None


class OrganizationDetailResponseSchema(BaseModel):
    id: int
    name: str
    phones: list[str]
    building: BuildingResponseSchema
    activities: list[OrganizationActivityResponseSchema]


class OrganizationDetailResponse(BaseResponseModel):
    result: OrganizationDetailResponseSchema


class OrganizationListResponse(BaseResponseModel):
    result: list[OrganizationShortResponseSchema]


class OrganizationInRadiusResponseSchema(BaseModel):
    id: int
    name: str
    building_id: int
    address: str
    distance_m: float


class OrganizationInRadiusListResponse(BaseResponseModel):
    result: list[OrganizationInRadiusResponseSchema]


class OrganizationInBboxListResponse(BaseResponseModel):
    result: list[OrganizationShortResponseSchema]


class ActivityResponse(
    BaseModel,
):
    id: int
    name: str
    path: str
    parent_id: int | None = None


class ActivityListResponse(BaseResponseModel):
    result: list[ActivityResponse]


class OrganizationByActivitySubtreeResponseSchema(OrganizationShortResponseSchema):
    activity_id: int
    root_path: str


class OrganizationByActivitySubtreeResponse(BaseResponseModel):
    result: list[OrganizationShortResponseSchema]
