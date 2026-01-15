from sqlalchemy import Integer, Text, ForeignKey, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import LtreeType

from core.db.accessor import Base
from core.db.mixins.timestamp_mixin import TimestampMixin


class Activity(Base, TimestampMixin):
    __tablename__ = "activity"

    MAX_DEPTH = 3  # Ограничение по ТЗ, но пожеланию можно сделать бесконечное дерево

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

    @classmethod
    def validate_path_depth(cls, path: str, max_depth: int = 3) -> bool:
        """Проверяет, что глубина пути не превышает max_depth уровней."""
        depth = len(str(path).split("."))
        return depth <= cls.MAX_DEPTH


@event.listens_for(Activity, "before_insert")
@event.listens_for(Activity, "before_update")
def validate_activity_depth(mapper, connection, target):
    """Валидация глубины вложенности перед вставкой/обновлением."""
    if not Activity.validate_path_depth(target.path):
        raise IntegrityError(f"Activity path depth exceeds maximum of 3 levels. Path: {target.path}", None, None)
