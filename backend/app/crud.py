"""Database helpers."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def create_shop(db: Session, data: schemas.ShopCreate) -> models.Shop:
    dishes = [models.Dish(**d.model_dump()) for d in data.dishes]
    shop = models.Shop(**data.model_dump(exclude={"dishes"}), dishes=dishes)
    db.add(shop)
    db.commit()
    db.refresh(shop)
    return shop


def get_shop(db: Session, shop_id: int) -> models.Shop | None:
    return db.get(models.Shop, shop_id)


def list_shops(db: Session) -> list[models.Shop]:
    return list(db.scalars(select(models.Shop).order_by(models.Shop.id)).all())


def get_twins(db: Session, shop_type: str | None = None) -> list[models.TwinShop]:
    stmt = select(models.TwinShop)
    if shop_type:
        stmt = stmt.where(models.TwinShop.shop_type == shop_type)
    return list(db.scalars(stmt).all())


def count_twins(db: Session) -> int:
    return len(db.scalars(select(models.TwinShop)).all())
