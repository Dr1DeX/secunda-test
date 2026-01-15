from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    limit: int = Field(default=10, ge=1, le=100, description="Number of items per page")
    offset: int = Field(default=0, ge=0, description="Offset for pagination")


class OrganizationSearchParams(PaginationParams):
    name: str = Field(..., min_length=1, description="Organization name to search")


class OrganizationsInRadiusParams(PaginationParams):
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")
    radius_m: float = Field(..., gt=0, description="Radius in meters")


class OrganizationsInBboxParams(PaginationParams):
    min_lat: float = Field(..., ge=-90, le=90, description="Minimum latitude")
    min_lon: float = Field(..., ge=-180, le=180, description="Minimum longitude")
    max_lat: float = Field(..., ge=-90, le=90, description="Maximum latitude")
    max_lon: float = Field(..., ge=-180, le=180, description="Maximum longitude")
