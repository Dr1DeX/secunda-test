from pydantic import BaseModel


class BuildingResponse(BaseModel):
    id: int
    address: str
    lat: float | None = None
    lon: float | None = None


class BuildingListResponse(BaseModel):
    items: list[BuildingResponse]


class OrganizationShortResponse(BaseModel):
    id: int
    name: str


class OrganizationPhoneResponse(BaseModel):
    phone: str


class OrganizationActivityResponse(BaseModel):
    id: int
    name: str
    path: str
    level: int | None = None


class OrganizationDetailResponse(BaseModel):
    id: int
    name: str
    phones: list[str]
    building: BuildingResponse
    activities: list[OrganizationActivityResponse]


class OrganizationListResponse(BaseModel):
    items: list[OrganizationShortResponse]


class OrganizationInRadiusResponse(BaseModel):
    id: int
    name: str
    building_id: int
    address: str
    distance_m: float


class OrganizationInRadiusListResponse(BaseModel):
    center: dict
    radius_m: float
    items: list[OrganizationInRadiusResponse]


class OrganizationInBboxListResponse(BaseModel):
    bbox: dict
    items: list[OrganizationShortResponse]


# Activity schemas
class ActivityResponse(BaseModel):
    id: int
    name: str
    path: str
    parent_id: int | None = None


class ActivityListResponse(BaseModel):
    items: list[ActivityResponse]


class OrganizationByActivitySubtreeResponse(BaseModel):
    activity_id: int
    root_path: str
    items: list[OrganizationShortResponse]
