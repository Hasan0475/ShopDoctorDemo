"""ORM models: Shop, Dish, TwinShop (benchmark dataset)."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Shop(Base):
    __tablename__ = "shops"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    shop_type: Mapped[str] = mapped_column(String(60), default="Cha chaan teng")
    district: Mapped[str] = mapped_column(String(60), default="Sham Shui Po")
    years_open: Mapped[int] = mapped_column(Integer, default=1)

    open_time: Mapped[str] = mapped_column(String(5), default="07:00")
    close_time: Mapped[str] = mapped_column(String(5), default="18:00")
    days_per_week: Mapped[int] = mapped_column(Integer, default=6)
    peak_period: Mapped[str] = mapped_column(String(20), default="Lunch")

    monthly_revenue: Mapped[float] = mapped_column(Float, default=0.0)
    monthly_rent: Mapped[float] = mapped_column(Float, default=0.0)
    monthly_staff_cost: Mapped[float] = mapped_column(Float, default=0.0)
    ingredient_pct: Mapped[float] = mapped_column(Float, default=0.0)
    waste_pct: Mapped[float] = mapped_column(Float, default=0.0)
    menu_size: Mapped[int] = mapped_column(Integer, default=0)

    google_maps_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    menu_photo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    storefront_photo_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    dishes: Mapped[list["Dish"]] = relationship(
        back_populates="shop", cascade="all, delete-orphan", lazy="selectin"
    )


class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(120))
    price: Mapped[float] = mapped_column(Float, default=0.0)
    cost: Mapped[float] = mapped_column(Float, default=0.0)
    units_per_month: Mapped[int] = mapped_column(Integer, default=0)
    share_pct: Mapped[float] = mapped_column(Float, default=0.0)

    shop: Mapped["Shop"] = relationship(back_populates="dishes")


class TwinShop(Base):
    """Benchmark records of similar shops: survived or closed after 2 years."""

    __tablename__ = "twin_shops"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    shop_type: Mapped[str] = mapped_column(String(60), default="Cha chaan teng")
    district: Mapped[str] = mapped_column(String(60), default="Kowloon")
    outcome: Mapped[str] = mapped_column(String(10))  # "survived" | "closed"
    trait: Mapped[str] = mapped_column(String(200), default="")
    avg_margin: Mapped[float] = mapped_column(Float, default=0.0)
    waste_pct: Mapped[float] = mapped_column(Float, default=0.0)
    menu_size: Mapped[int] = mapped_column(Integer, default=0)
