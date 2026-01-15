from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import LtreeType

from core.db.accessor import Base
from core.db.mixins.timestamp_mixin import TimestampMixin


class Activity(Base, TimestampMixin):
    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    # materialized path (ltree): Для эффективного хранения древовидной структуры
    path: Mapped[str] = mapped_column(LtreeType, nullable=False, unique=True)

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("activity.id"), nullable=True)

    parent = relationship("Activity", remote_side=[id], backref="children")

    organizations = relationship(
        "Organization",
        secondary="organization_activity",
        back_populates="activities",
    )
