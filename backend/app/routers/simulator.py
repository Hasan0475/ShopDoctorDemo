"""Price Simulator endpoint."""
from __future__ import annotations

from fastapi import APIRouter

from .. import schemas
from ..agents import simulate_price
from ..config import settings

router = APIRouter(tags=["simulator"])


@router.post("/simulator", response_model=schemas.SimulatorOut)
def run_simulator(payload: schemas.SimulatorIn) -> schemas.SimulatorOut:
    elasticity = settings.default_elasticity if payload.elasticity is None else payload.elasticity
    res = simulate_price(
        dish=payload.dish,
        base_price=payload.base_price,
        base_cost=payload.base_cost,
        base_units=payload.base_units,
        new_price=payload.price,
        elasticity=elasticity,
    )
    return schemas.SimulatorOut(
        dish=payload.dish,
        base_price=payload.base_price,
        new_price=payload.price,
        elasticity=elasticity,
        base_units=res.base_units,
        new_units=res.new_units,
        base_margin_pct=res.base_margin_pct,
        new_margin_pct=res.new_margin_pct,
        before_profit=res.before_profit,
        after_profit=res.after_profit,
        profit_delta=res.profit_delta,
        direction=res.direction,
        advice_title=res.advice_title,
        advice=res.advice,
    )
