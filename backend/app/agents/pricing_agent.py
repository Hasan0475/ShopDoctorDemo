"""Pricing agent — deterministic demand/elasticity simulator.

Pure maths (no LLM needed) so results are stable and testable:

    units(new_price) = base_units * (new_price / base_price) ** elasticity

with a default elasticity of -1.4 estimated from the twin-shop dataset.
"""
from __future__ import annotations

from dataclasses import dataclass

from ..config import settings


@dataclass
class SimResult:
    base_units: int
    new_units: int
    base_margin_pct: int
    new_margin_pct: int
    before_profit: float
    after_profit: float
    profit_delta: float
    direction: str
    advice_title: str
    advice: str


def simulate_price(
    dish: str,
    base_price: float,
    base_cost: float,
    base_units: int,
    new_price: float,
    elasticity: float | None = None,
) -> SimResult:
    e = settings.default_elasticity if elasticity is None else elasticity
    base_price = max(base_price, 0.01)
    new_price = max(new_price, 0.01)

    ratio = new_price / base_price
    new_units = max(0, int(round(base_units * (ratio ** e))))

    before_profit = (base_price - base_cost) * base_units
    after_profit = (new_price - base_cost) * new_units
    delta = after_profit - before_profit

    base_margin = (base_price - base_cost) / base_price if base_price else 0.0
    new_margin = (new_price - base_cost) / new_price if new_price else 0.0

    threshold = abs(before_profit) * 0.02 or 1.0
    if abs(delta) < threshold:
        direction = "flat"
        title = "Roughly break-even"
        advice = (
            "This price keeps monthly profit about the same — decide based on "
            "traffic and positioning rather than margin."
        )
    elif delta > 0:
        direction = "up"
        title = "Raise the price"
        lost = max(0, base_units - new_units)
        advice = (
            f"At HK${new_price:.0f} you'd earn about HK${delta:,.0f} more per month, "
            f"even after losing ~{lost:,} units."
        )
    else:
        direction = "down"
        title = "This cuts profit"
        advice = (
            f"At HK${new_price:.0f} you'd lose about HK${abs(delta):,.0f} per month — "
            "the volume drop outweighs the extra margin."
        )

    return SimResult(
        base_units=base_units,
        new_units=new_units,
        base_margin_pct=int(round(base_margin * 100)),
        new_margin_pct=int(round(new_margin * 100)),
        before_profit=round(before_profit, 2),
        after_profit=round(after_profit, 2),
        profit_delta=round(delta, 2),
        direction=direction,
        advice_title=title,
        advice=advice,
    )
