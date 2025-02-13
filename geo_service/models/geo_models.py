import datetime

from sqlalchemy import String, Float, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from core import Base


class Geo(Base):
    __tablename__ = "geo"

    cadastre_number: Mapped[str] = mapped_column(String, nullable=False, name="cadastre_number")
    latitude: Mapped[float] = mapped_column(Float, nullable=False, name="latitude")
    longitude: Mapped[float] = mapped_column(Float, nullable=False, name="longitude")
    result: Mapped[bool] = mapped_column(Boolean, nullable=True, name="result")
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.UTC),
        name="created_at",
    )

    def __repr__(self):
        return (
            f"Geo(id={self.id}, cadastre_number={self.cadastre_number}, "
            f"latitude={self.latitude}, longitude={self.longitude}, result={self.result})"
        )