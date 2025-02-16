import datetime

from sqlalchemy import String, DateTime, ForeignKey, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core import Base


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="role",
        lazy="selectin"
    )

    def __repr__(self):
        return self.name


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc)
    )
    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role: Mapped["Role"] = relationship("Role", back_populates="users", lazy="selectin")


    def __repr__(self):
        return self.username
