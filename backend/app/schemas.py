"""Pydantic schemas (request/response contracts)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ---------- Inputs ----------
class DishIn(BaseModel):
    name: str
    price: float = Field(ge=0)
    cost: float = Field(ge=0)
    units_per_month: int = Field(default=0, ge=0)
    share_pct: float = Field(default=0.0, ge=0, le=100)


class ShopCreate(BaseModel):
    name: str
    shop_type: str = "Cha chaan teng"
    district: str = "Sham Shui Po"
    years_open: int = Field(default=1, ge=0)
    open_time: str = "07:00"
    close_time: str = "18:00"
    days_per_week: int = Field(default=6, ge=0, le=7)
    peak_period: str = "Lunch"
    monthly_revenue: float = Field(default=0.0, ge=0)
    monthly_rent: float = Field(default=0.0, ge=0)
    monthly_staff_cost: float = Field(default=0.0, ge=0)
    ingredient_pct: float = Field(default=0.0, ge=0, le=100)
    waste_pct: float = Field(default=0.0, ge=0, le=100)
    menu_size: int = Field(default=0, ge=0)
    google_maps_url: str | None = None
    menu_photo_url: str | None = None
    storefront_photo_url: str | None = None
    dishes: list[DishIn] = Field(default_factory=list)


class SimulatorIn(BaseModel):
    dish: str
    base_price: float = Field(gt=0)
    base_cost: float = Field(ge=0)
    base_units: int = Field(default=1000, ge=0)
    price: float = Field(gt=0)
    elasticity: float | None = None


class ChatIn(BaseModel):
    message: str
    lang: str = Field(default="en", pattern="^(en|zh)$")
    shop_id: int | None = None


# ---------- Outputs ----------
class DishOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    price: float
    cost: float
    units_per_month: int
    share_pct: float
    margin: float
    margin_pct: int
    status: str


class MetricOut(BaseModel):
    label: str
    value: str
    tone: str = "neutral"  # neutral | good | warn | bad


class ProblemOut(BaseModel):
    icon: str
    title: str
    detail: str
    severity: str = "warn"


class TwinOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    trait: str


class TwinGroups(BaseModel):
    survivors: list[TwinOut]
    closed: list[TwinOut]
    survivors_count: int
    closed_count: int


class ReportOut(BaseModel):
    shop_id: int
    shop_name: str
    health_score: int
    score_band: str  # healthy | watch | at-risk
    summary: str
    metrics: list[MetricOut]
    dishes: list[DishOut]
    problems: list[ProblemOut]
    twins: TwinGroups
    diagnosis: str


class ShopOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    shop_type: str
    district: str
    years_open: int
    monthly_revenue: float
    created_at: datetime


class SimulatorOut(BaseModel):
    dish: str
    base_price: float
    new_price: float
    elasticity: float
    base_units: int
    new_units: int
    base_margin_pct: int
    new_margin_pct: int
    before_profit: float
    after_profit: float
    profit_delta: float
    direction: str  # up | down | flat
    advice_title: str
    advice: str


class ChatOut(BaseModel):
    reply: str
    lang: str
    intent: str


class MarketingPost(BaseModel):
    emoji: str
    title: str
    rationale: str
    caption: str


class MarketingOut(BaseModel):
    shop_id: int | None
    posts: list[MarketingPost]


class HealthOut(BaseModel):
    status: str
    version: str
    llm_provider: str
