"""Marketing Kit endpoint."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..agents import generate_posts
from ..database import get_db

router = APIRouter(tags=["marketing"])


@router.get("/shops/{shop_id}/marketing", response_model=schemas.MarketingOut)
def marketing(shop_id: int, limit: int = 4, db: Session = Depends(get_db)):
    shop = crud.get_shop(db, shop_id)
    if not shop:
        raise HTTPException(404, "Shop not found")
    posts = generate_posts(shop.name, shop.dishes, limit=limit)
    return schemas.MarketingOut(
        shop_id=shop.id, posts=[schemas.MarketingPost(**p) for p in posts]
    )
