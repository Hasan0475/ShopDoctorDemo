"""Ask Shop Doctor — bilingual follow-up chat."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..agents import chat_answer
from ..database import get_db
from ..services import build_report, report_as_text

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=schemas.ChatOut)
def chat(payload: schemas.ChatIn, db: Session = Depends(get_db)):
    context = None
    if payload.shop_id:
        shop = crud.get_shop(db, payload.shop_id)
        if shop:
            context = report_as_text(build_report(db, shop))

    reply, intent = chat_answer(payload.message, payload.lang, context)
    return schemas.ChatOut(reply=reply, lang=payload.lang, intent=intent)
