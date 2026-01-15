from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text, func
from sqlalchemy.orm import selectinload

from geoalchemy2.functions import ST_X, ST_Y

from core.db.models.activity import Activity
from core.db.models.building import Building
from core.db.models.organization import Organization


@dataclass
class DirectoryRepository:
    _session: AsyncSession

    async def get_organization_by_id(self, organization_id: int):
        stmt = (
            select(Organization)
            .where(Organization.id == organization_id)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.activities),
            )
        )

        org = (await self._session.execute(stmt)).scalar_one_or_none()

        if not org:
            return None

        building = org.building
        coords_stmt = select(
            ST_Y(building.location).label("lat"),
            ST_X(building.location).label("lon"),
        ).where(Building.id == building.id)
        coords = (await self._session.execute(coords_stmt)).mappings().first()
        return dict(
            id=org.id,
            name=org.name,
            phones=[p.phone for p in org.phones],
            building=dict(
                id=building.id,
                address=building.address,
                lat=coords["lat"] if coords else None,
                lon=coords["lon"] if coords else None,
            ),
            activities=[dict(id=a.id, name=a.name, path=str(a.path), level=None) for a in org.activities],
        )

    async def get_list_buildings(
        self,
        limit: int = 10,
        offset: int = 0,
    ):
        stmt = (
            select(
                Building.id,
                Building.address,
                ST_Y(Building.location).label("lat"),
                ST_X(Building.location).label("lon"),
            )
            .order_by(Building.id)
            .limit(limit)
            .offset(offset)
        )

        rows = (await self._session.execute(stmt)).mappings().all()
        return dict(items=list(rows))

    async def get_list_organizations_by_building(self, building_id: int, limit: int = 10, offset: int = 0):
        stmt = (
            select(Organization.id, Organization.name)
            .where(Organization.building_id == building_id)
            .order_by(Organization.id)
            .limit(limit)
            .offset(offset)
        )

        rows = (await self._session.execute(stmt)).mappings().all()
        return dict(items=list(rows))

    async def get_list_organizations_by_activity_exact(self, activity_id: int, limit: int = 10, offset: int = 0):
        stmt = (
            select(Organization.id, Organization.name)
            .join(Organization.activities)
            .where(Activity.id == activity_id)
            .order_by(Organization.id)
            .limit(limit)
            .offset(offset)
        )

        rows = (await self._session.execute(stmt)).mappings().all()
        return dict(items=list(rows))

    async def get_organizations_by_activity_subtree(self, activity_id: int, limit: int = 10, offset: int = 0):
        root_stmt = select(Activity.path).where(Activity.id == activity_id)

        root_path = (await self._session.execute(root_stmt)).scalar_one_or_none()

        if not root_path:
            return None

        stmt = (
            select(Organization.id, Organization.name)
            .join(Organization.activities)
            .where(text("activity.path <@ :root_path"))  # ltree operator: <@ (is descendant or equal)
            .params(root_path=str(root_path))
            .distinct()
            .order_by(Organization.id)
            .limit(limit)
            .offset(offset)
        )

        rows = (await self._session.execute(stmt)).mappings().all()
        return dict(
            activity_id=activity_id,
            root_path=str(root_path),
            items=list(rows),
        )

    async def get_organizations_by_name(self, name: str, limit: int = 10, offset: int = 0):
        stmt = (
            select(Organization.id, Organization.name)
            .where(Organization.name.ilike(f"%{name}%"))
            .order_by(Organization.id)
            .limit(limit)
            .offset(offset)
        )

        rows = (await self._session.execute(stmt)).mappings().all()
        return dict(items=list(rows))

    async def get_organizations_in_radius(
        self,
        lat: float,
        lon: float,
        radius_m: float,
        limit: int = 10,
        offset: int = 0,
    ):
        point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
        point_geog = func.ST_GeogFromText(func.ST_AsText(point))

        stmt = (
            select(
                Organization.id,
                Organization.name,
                Building.id.label("building_id"),
                Building.address,
                func.ST_Distance(Building.location, point_geog).label("distance_m"),
            )
            .join(Building, Organization.building_id == Building.id)
            .where(func.ST_DWithin(Building.location, point_geog, radius_m))
            .order_by(text("distance_m ASC"))
            .limit(limit)
            .offset(offset)
        )

        rows = (await self._session.execute(stmt)).mappings().all()
        return dict(
            center=dict(lat=lat, lon=lon),
            radius_m=radius_m,
            items=list(rows),
        )

    async def get_organizations_in_bbox(
        self,
        min_lat: float,
        min_lon: float,
        max_lat: float,
        max_lon: float,
        limit: int = 10,
        offset: int = 0,
    ):
        env = func.ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, 4326)
        env_geog = func.ST_GeogFromText(func.ST_AsText(env))

        stmt = (
            select(
                Organization.id,
                Organization.name,
                Building.id.label("building_id"),
                Building.address,
            )
            .join(Building, Organization.building_id == Building.id)
            .where(func.ST_Intersects(Building.location, env_geog))
            .order_by(Organization.id)
            .limit(limit)
            .offset(offset)
        )

        rows = (await self._session.execute(stmt)).mappings().all()
        return dict(
            bbox=dict(
                min_lat=min_lat,
                min_lon=min_lon,
                max_lat=max_lat,
                max_lon=max_lon,
            ),
            items=list(rows),
        )

    async def get_list_activities(self):
        stmt = select(Activity.id, Activity.name, Activity.path, Activity.parent_id).order_by(Activity.id)

        rows = (await self._session.execute(stmt)).mappings().all()
        return dict(
            items=list(dict(id=r["id"], name=r["name"], path=str(r["path"]), parent_id=r["parent_id"]) for r in rows),
        )
