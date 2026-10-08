"""Diagnosis agent — turns a shop's numbers into a Health Score, per-dish
margins, ranked problems, and a written diagnosis benchmarked against twins.

The scoring is fully deterministic (so it is testable and explainable); the
optional LLM provider is only used to add narrative polish when a real key is
configured.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .base import get_provider


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def dish_margin(price: float, cost: float) -> float:
    return (price - cost) / price if price > 0 else 0.0


def dish_status(margin: float) -> str:
    if margin >= 0.55:
        return "healthy"
    if margin >= 0.35:
        return "thin"
    return "losing"


@dataclass
class DishDiag:
    name: str
    price: float
    cost: float
    units_per_month: int
    share_pct: float
    margin: float
    margin_pct: int
    status: str


@dataclass
class Problem:
    icon: str
    title: str
    detail: str
    severity: str = "warn"


@dataclass
class Diagnosis:
    health_score: int
    score_band: str
    summary: str
    metrics: list[dict] = field(default_factory=list)
    dishes: list[DishDiag] = field(default_factory=list)
    problems: list[Problem] = field(default_factory=list)
    diagnosis_text: str = ""


# Healthy / bad thresholds for HK F&B, used to score each component 0..100.
RENT_GOOD, RENT_BAD = 0.22, 0.38
LABOR_GOOD, LABOR_BAD = 0.25, 0.42
COGS_GOOD, COGS_BAD = 0.28, 0.40
WASTE_GOOD, WASTE_BAD = 4.0, 11.0
MARGIN_GOOD, MARGIN_BAD = 0.58, 0.32


def _band_score(value: float, good: float, bad: float) -> float:
    """100 when at/better than `good`, 0 when at/worse than `bad`."""
    if bad == good:
        return 100.0
    return _clamp((bad - value) / (bad - good)) * 100.0


def diagnose(shop, dishes, benchmark: dict) -> Diagnosis:
    revenue = shop.monthly_revenue or 0.0

    # --- per-dish margins -------------------------------------------------
    dish_diags: list[DishDiag] = []
    for d in dishes:
        m = dish_margin(d.price, d.cost)
        dish_diags.append(
            DishDiag(
                name=d.name,
                price=d.price,
                cost=d.cost,
                units_per_month=d.units_per_month,
                share_pct=d.share_pct,
                margin=round(m, 4),
                margin_pct=int(round(m * 100)),
                status=dish_status(m),
            )
        )

    # --- component scores -------------------------------------------------
    rent_ratio = shop.monthly_rent / revenue if revenue else 0
    labor_ratio = shop.monthly_staff_cost / revenue if revenue else 0
    cogs_ratio = (shop.ingredient_pct or 0) / 100.0

    margins = [d.margin for d in dish_diags] or [0.0]
    avg_margin = sum(margins) / len(margins)
    losing_count = sum(1 for d in dish_diags if d.status == "losing")

    rent_score = _band_score(rent_ratio, RENT_GOOD, RENT_BAD)
    labor_score = _band_score(labor_ratio, LABOR_GOOD, LABOR_BAD)
    cogs_score = _band_score(cogs_ratio, COGS_GOOD, COGS_BAD)
    waste_score = _band_score(shop.waste_pct or 0, WASTE_GOOD, WASTE_BAD)
    margin_score = _band_score(avg_margin, MARGIN_BAD, MARGIN_GOOD)

    health = (
        0.30 * margin_score
        + 0.20 * rent_score
        + 0.18 * labor_score
        + 0.17 * cogs_score
        + 0.15 * waste_score
    )
    health_score = int(round(health))

    if health_score >= 75:
        band = "healthy"
    elif health_score >= 60:
        band = "watch"
    else:
        band = "at-risk"

    # --- net margin & prediction -----------------------------------------
    ingredient_cost = revenue * cogs_ratio
    waste_cost = ingredient_cost * (shop.waste_pct or 0) / 100.0
    net = revenue - shop.monthly_rent - shop.monthly_staff_cost - ingredient_cost - waste_cost
    net_margin = net / revenue if revenue else 0.0

    # Simple forward projection: shops in the bottom band trend down.
    if band == "at-risk":
        trend = -0.11
    elif band == "watch":
        trend = -0.03
    else:
        trend = 0.05

    metrics = [
        {"label": "Monthly revenue", "value": f"HK${revenue:,.0f}", "tone": "neutral"},
        {"label": "Net margin", "value": f"{net_margin*100:.1f}%",
         "tone": "bad" if net_margin < 0.06 else ("warn" if net_margin < 0.12 else "good")},
        {"label": "Predicted revenue (6 mo)", "value": f"{trend*100:+.0f}%",
         "tone": "bad" if trend < 0 else "good"},
        {"label": "Avg dish margin", "value": f"{avg_margin*100:.0f}%",
         "tone": "good" if avg_margin >= 0.55 else ("warn" if avg_margin >= 0.35 else "bad")},
        {"label": "Rent / revenue", "value": f"{rent_ratio*100:.0f}%",
         "tone": "good" if rent_ratio <= RENT_GOOD else ("bad" if rent_ratio >= RENT_BAD else "warn")},
        {"label": "Dishes losing money", "value": f"{losing_count} of {len(dish_diags)}",
         "tone": "bad" if losing_count else "good"},
    ]

    # --- problems (ranked) ------------------------------------------------
    problems: list[Problem] = []

    losing_dishes = sorted(
        [d for d in dish_diags if d.status == "losing"], key=lambda d: d.margin
    )
    if losing_dishes:
        names = ", ".join(d.name for d in losing_dishes[:2])
        problems.append(
            Problem(
                "🩸",
                "Some dishes barely break even",
                f"{len(losing_dishes)} dish(es) sit under a 20% margin — {names}. "
                "Surviving twin shops cut or repriced items like these. Reprice or "
                "renegotiate ingredient cost.",
                "bad",
            )
        )

    thin_high_share = [
        d for d in dish_diags if d.status == "thin" and d.share_pct >= 12
    ]
    if thin_high_share:
        d = max(thin_high_share, key=lambda x: x.share_pct)
        problems.append(
            Problem(
                "🥩",
                "A top seller is eating your margin",
                f"{d.name} is {d.share_pct:.0f}% of sales at only {d.margin_pct}% margin. "
                f"Raising it toward HK${round(d.price*1.12)} or cutting cost is your "
                "single biggest profit lever.",
                "warn",
            )
        )

    surv_waste = benchmark.get("survivor_waste", 4.5)
    if (shop.waste_pct or 0) > surv_waste + 2:
        problems.append(
            Problem(
                "🗑️",
                f"Weekday waste is {shop.waste_pct:.0f}%",
                f"Surviving twin shops average ~{surv_waste:.0f}%. Trimming prep on slow "
                f"weekday afternoons could save roughly HK${revenue*cogs_ratio*(shop.waste_pct-surv_waste)/100:,.0f}/month.",
                "warn",
            )
        )

    if rent_ratio >= RENT_BAD:
        problems.append(
            Problem(
                "🏠",
                f"Rent is {rent_ratio*100:.0f}% of revenue",
                "Above the ~22-25% that survivors sustain. Grow revenue per seat "
                "(sets, higher-margin heroes, extra dayparts) rather than absorbing it.",
                "bad",
            )
        )

    stars = [d for d in dish_diags if d.status == "healthy"]
    if stars:
        star_names = ", ".join(d.name for d in sorted(stars, key=lambda x: -x.margin)[:2])
        problems.append(
            Problem(
                "📣",
                "Your stars are under-promoted",
                f"{star_names} carry your healthiest margins. Push them in the Marketing "
                "Kit and as set-meal anchors to shift mix toward profit.",
                "good",
            )
        )

    # --- narrative --------------------------------------------------------
    surv_m = benchmark.get("survivor_margin", 0.55)
    closed_m = benchmark.get("closed_margin", 0.30)
    position = "closer to the closed group" if avg_margin < (surv_m + closed_m) / 2 else "closer to the survivors"
    diagnosis_text = (
        f"ShopDoctor scored {shop.name} at {health_score}/100 ({band}). Your average dish "
        f"margin is {avg_margin*100:.0f}%, versus ~{surv_m*100:.0f}% for surviving twin shops and "
        f"~{closed_m*100:.0f}% for those that closed — putting you {position}. "
        f"The biggest levers, in order: {', '.join(p.title.lower() for p in problems[:3]) or 'tighten dish margins'}."
    )

    summary = (
        f"{health_score}/100 — {band.replace('-', ' ')}. Net margin {net_margin*100:.1f}%, "
        f"{losing_count} dish(es) losing money."
    )

    # Optional LLM polish (no-op with the offline mock provider).
    provider = get_provider()
    if provider.name != "mock":
        try:
            diagnosis_text = provider.complete(
                f"Rewrite this shop diagnosis for a non-financial HK restaurant owner, "
                f"warm and concrete, keep all numbers:\n{diagnosis_text}",
                system="You are ShopDoctor, a business GP for small HK restaurants.",
            )
        except Exception:  # pragma: no cover - network path
            pass

    return Diagnosis(
        health_score=health_score,
        score_band=band,
        summary=summary,
        metrics=metrics,
        dishes=dish_diags,
        problems=problems,
        diagnosis_text=diagnosis_text,
    )
