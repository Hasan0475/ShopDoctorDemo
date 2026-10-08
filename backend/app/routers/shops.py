"""Shops CRUD + twins listing."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..agents import benchmark_stats, find_twins
from ..database import get_db

router = APIRouter(prefix="/shops", tags=["shops"])


@router.get("", response_model=list[schemas.ShopOut])
def list_shops(db: Session = Depends(get_db)):
    return crud.list_shops(db)


@router.post("", response_model=schemas.ShopOut, status_code=201)
def create_shop(payload: schemas.ShopCreate, db: Session = Depends(get_db)):
    shop = crud.create_shop(db, payload)
    return shop


@router.get("/{shop_id}", response_model=schemas.ShopOut)
def get_shop(shop_id: int, db: Session = Depends(get_db)):
    shop = crud.get_shop(db, shop_id)
    if not shop:
        raise HTTPException(404, "Shop not found")
    return shop


@router.get("/{shop_id}/twins", response_model=schemas.TwinGroups)
def get_twins(shop_id: int, db: Session = Depends(get_db)):
    shop = crud.get_shop(db, shop_id)
    if not shop:
        raise HTTPException(404, "Shop not found")
    rows = crud.get_twins(db, shop.shop_type)
    groups = find_twins(rows)
    return schemas.TwinGroups(
        survivors=[schemas.TwinOut(name=t.name, trait=t.trait) for t in groups.survivors],
        closed=[schemas.TwinOut(name=t.name, trait=t.trait) for t in groups.closed],
        survivors_count=groups.survivors_count,
        closed_count=groups.closed_count,
    )


@router.get("/meta/benchmark")
def get_benchmark(shop_type: str = "Cha chaan teng", db: Session = Depends(get_db)):
    rows = crud.get_twins(db, shop_type)
    return benchmark_stats(rows)
