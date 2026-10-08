"""Report service — orchestrates the agents to build a full Health Report."""
from __future__ import annotations

from sqlalchemy.orm import Session

from . import crud, models, schemas
from .agents import benchmark_stats, diagnose, find_twins


def build_report(db: Session, shop: models.Shop) -> schemas.ReportOut:
    twins_rows = crud.get_twins(db, shop.shop_type)
    benchmark = benchmark_stats(twins_rows)
    groups = find_twins(twins_rows)

    diag = diagnose(shop, shop.dishes, benchmark)

    dishes = [
        schemas.DishOut(
            id=i + 1,
            name=d.name,
            price=d.price,
            cost=d.cost,
            units_per_month=d.units_per_month,
            share_pct=d.share_pct,
            margin=d.margin,
            margin_pct=d.margin_pct,
            status=d.status,
        )
        for i, d in enumerate(diag.dishes)
    ]

    return schemas.ReportOut(
        shop_id=shop.id,
        shop_name=shop.name,
        health_score=diag.health_score,
        score_band=diag.score_band,
        summary=diag.summary,
        metrics=[schemas.MetricOut(**m) for m in diag.metrics],
        dishes=dishes,
        problems=[schemas.ProblemOut(**p.__dict__) for p in diag.problems],
        twins=schemas.TwinGroups(
            survivors=[schemas.TwinOut(name=t.name, trait=t.trait) for t in groups.survivors],
            closed=[schemas.TwinOut(name=t.name, trait=t.trait) for t in groups.closed],
            survivors_count=groups.survivors_count,
            closed_count=groups.closed_count,
        ),
        diagnosis=diag.diagnosis_text,
    )


def report_as_text(report: schemas.ReportOut) -> str:
    """Compact text form used as chat context."""
    lines = [
        f"Shop: {report.shop_name}",
        f"Health score: {report.health_score}/100 ({report.score_band})",
        "Metrics: " + "; ".join(f"{m.label}={m.value}" for m in report.metrics),
        "Dishes: "
        + "; ".join(
            f"{d.name} HK${d.price:.0f}/cost HK${d.cost:.0f}/{d.margin_pct}%/{d.status}"
            for d in report.dishes
        ),
        "Problems: " + "; ".join(p.title for p in report.problems),
    ]
    return "\n".join(lines)
