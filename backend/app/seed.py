"""Seed the database with a demo shop and the twin-shop benchmark dataset.

Run automatically on startup when the DB is empty (see ``main.py``), or
manually via ``python -m app.seed``.
"""
from __future__ import annotations

from sqlalchemy import select

from . import models
from .database import Base, SessionLocal, engine

DEMO_SHOP = {
    "name": "Ming Kee Cha Chaan Teng",
    "shop_type": "Cha chaan teng",
    "district": "Sham Shui Po",
    "years_open": 3,
    "open_time": "07:00",
    "close_time": "18:00",
    "days_per_week": 6,
    "peak_period": "Lunch",
    "monthly_revenue": 182000,
    "monthly_rent": 55000,
    "monthly_staff_cost": 68000,
    "ingredient_pct": 26,
    "waste_pct": 9,
    "menu_size": 12,
    "google_maps_url": "https://maps.google.com/?q=Sham+Shui+Po",
}

DEMO_DISHES = [
    # name, price, cost, units/month, share%
    ("Signature milk tea", 26, 8, 1850, 26),
    ("Pineapple bun w/ butter", 16, 5, 1600, 14),
    ("Beef brisket noodles", 52, 34, 630, 18),
    ("Ham & egg sandwich", 32, 26, 420, 7),
    ("Baked pork chop rice", 58, 29, 560, 18),
    ("Iced lemon tea", 22, 6, 700, 8),
    ("Egg tart", 10, 8, 400, 2),
    ("Club sandwich", 42, 39, 250, 6),
]

# Benchmark dataset: similar cha chaan tengs in Kowloon, split by 2-year outcome.
TWINS = [
    # name, outcome, trait, avg_margin, waste%, menu_size
    ("Kam Fat Café", "survived", "Short menu, 4 high-margin signature dishes", 0.58, 4.0, 14),
    ("Sun Wah Tea Room", "survived", "Cuts weekday prep 50% after 2pm", 0.55, 4.5, 18),
    ("Australia Dairy Co.", "survived", "Promotes hero items, high table turnover", 0.61, 3.8, 12),
    ("Yee Hung Dessert", "survived", "Tight COGS, single dessert focus", 0.63, 3.0, 10),
    ("Lan Kwai Teahouse", "survived", "Afternoon-tea set lifts ticket size", 0.54, 5.0, 16),
    ("Mido Café", "survived", "Loyal regulars, stable weekday demand", 0.52, 5.5, 15),
    ("Tung Kee Noodles", "survived", "Renegotiated supplier contracts yearly", 0.57, 4.2, 13),
    ("Happy V Cafe", "survived", "Tracks dish-level profit weekly", 0.56, 4.0, 17),
    ("Wing Kee", "closed", "40-item menu, average margins everywhere", 0.33, 8.0, 40),
    ("Happy Café", "closed", "No cost tracking, 9% weekday waste", 0.31, 9.5, 30),
    ("Sun Sing", "closed", "Underpriced noodles to chase traffic", 0.24, 7.0, 22),
    ("Golden Dragon Café", "closed", "High rent ratio, thin best-sellers", 0.29, 8.5, 26),
    ("Ocean Restaurant", "closed", "Never promoted its profitable dishes", 0.35, 7.5, 34),
    ("Wah On Café", "closed", "Slow movers kept on the menu for years", 0.27, 9.0, 28),
]


def seed(db=None) -> None:
    own_session = db is None
    if own_session:
        db = SessionLocal()
    try:
        if db.scalar(select(models.Shop).limit(1)) is None:
            shop = models.Shop(**DEMO_SHOP)
            shop.dishes = [
                models.Dish(name=n, price=p, cost=c, units_per_month=u, share_pct=s)
                for (n, p, c, u, s) in DEMO_DISHES
            ]
            db.add(shop)

        if db.scalar(select(models.TwinShop).limit(1)) is None:
            for name, outcome, trait, margin, waste, menu in TWINS:
                db.add(
                    models.TwinShop(
                        name=name,
                        shop_type="Cha chaan teng",
                        district="Kowloon",
                        outcome=outcome,
                        trait=trait,
                        avg_margin=margin,
                        waste_pct=waste,
                        menu_size=menu,
                    )
                )
        db.commit()
    finally:
        if own_session:
            db.close()


def reset_db() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_db()
    seed()
    print("Seeded demo shop + twin-shop benchmark dataset.")
