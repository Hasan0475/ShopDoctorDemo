"""Health Report endpoint (the diagnosis / prescription)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..services import build_report

router = APIRouter(prefix="/shops", tags=["report"])


@router.get("/{shop_id}/report", response_model=schemas.ReportOut)
def get_report(shop_id: int, db: Session = Depends(get_db)):
    shop = crud.get_shop(db, shop_id)
    if not shop:
        raise HTTPException(404, "Shop not found")
    return build_report(db, shop)
