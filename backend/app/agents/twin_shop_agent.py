"""Twin-shop agent — finds comparable shops and splits them into Survivors
(still open after 2 years) and Closed, the benchmark used for diagnosis."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Twin:
    name: str
    trait: str
    outcome: str


@dataclass
class TwinGroups:
    survivors: list[Twin]
    closed: list[Twin]

    @property
    def survivors_count(self) -> int:
        return len(self.survivors)

    @property
    def closed_count(self) -> int:
        return len(self.closed)


def find_twins(twin_rows: list) -> TwinGroups:
    """Group benchmark rows (models.TwinShop) by outcome."""
    survivors, closed = [], []
    for row in twin_rows:
        t = Twin(name=row.name, trait=row.trait, outcome=row.outcome)
        (survivors if row.outcome == "survived" else closed).append(t)
    return TwinGroups(survivors=survivors, closed=closed)


def benchmark_stats(twin_rows: list) -> dict:
    """Average margin / waste of survivors vs closed — the diagnostic signal."""

    def _avg(rows, attr):
        vals = [getattr(r, attr) for r in rows]
        return sum(vals) / len(vals) if vals else 0.0

    survivors = [r for r in twin_rows if r.outcome == "survived"]
    closed = [r for r in twin_rows if r.outcome == "closed"]
    return {
        "survivor_margin": _avg(survivors, "avg_margin"),
        "closed_margin": _avg(closed, "avg_margin"),
        "survivor_waste": _avg(survivors, "waste_pct"),
        "closed_waste": _avg(closed, "waste_pct"),
        "survivor_menu": _avg(survivors, "menu_size"),
        "closed_menu": _avg(closed, "menu_size"),
        "n_survivors": len(survivors),
        "n_closed": len(closed),
    }
