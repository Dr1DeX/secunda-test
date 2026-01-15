from core.db.accessor import Base
from core.db.mixins.timestamp_mixin import TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, ForeignKey, UniqueConstraint


class Organization(Base, TimestampMixin):
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False, index=True)

    building_id: Mapped[int] = mapped_column(ForeignKey("building.id"), nullable=False)
    building = relationship("Building", back_populates="organizations")

    phones = relationship("OrganizationPhone", back_populates="organization", cascade="all, delete-orphan")

    activities = relationship(
        "Activity",
        secondary="organization_activity",
        back_populates="organizations",
    )


class OrganizationPhone(Base):
    __tablename__ = "organization_phone"
    __table_args__ = (UniqueConstraint("organization_id", "phone", name="uq_org_phone"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)
    phone: Mapped[str] = mapped_column(Text, nullable=False)

    organization = relationship("Organization", back_populates="phones")


class OrganizationActivity(Base):
    __tablename__ = "organization_activity"

    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), primary_key=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey("activity.id"), primary_key=True)
