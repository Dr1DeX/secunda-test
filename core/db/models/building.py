from core.db.accessor import Base
from core.db.mixins.timestamp_mixin import TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text
from geoalchemy2 import Geography


class Building(Base, TimestampMixin):
    __tablename__ = "building"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(Text, nullable=False)

    # geography(Point, 4326) — удобнее для расстояний в метрах
    location: Mapped[object] = mapped_column(
        Geography(geometry_type="POINT", srid=4326),
        nullable=False,
    )

    organizations = relationship("Organization", back_populates="building")
