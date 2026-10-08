"""Marketing agent — generates Instagram post ideas, captions and photo briefs
that favour the shop's highest-margin dishes."""
from __future__ import annotations

from .base import get_provider

EMOJI_BY_KEYWORD = [
    (("tea", "茶"), "🧋"),
    (("bun", "菠蘿", "toast", "多士"), "🍍"),
    (("noodle", "麵", "粉"), "🍜"),
    (("rice", "飯"), "🍚"),
    (("sandwich", "三文治"), "🥪"),
    (("tart", "撻", "dessert", "甜品"), "🥧"),
    (("coffee", "咖啡"), "☕"),
    (("lemon", "檸"), "🍋"),
]


def _emoji_for(name: str) -> str:
    lower = name.lower()
    for keys, emoji in EMOJI_BY_KEYWORD:
        if any(k in lower for k in keys):
            return emoji
    return "🍽️"


def _caption(name: str, shop_name: str) -> str:
    return (
        f"Fresh, local, and made the way {shop_name} has always done it. "
        f"Come taste our {name} — you'll be back tomorrow. "
        f"#HKFood #ChaChaanTeng #SupportLocal #{name.replace(' ', '')}"
    )


def generate_posts(shop_name: str, dishes: list, limit: int = 4) -> list[dict]:
    """Build post ideas from the highest-margin dishes."""
    ranked = sorted(
        dishes,
        key=lambda d: ((d.price - d.cost) / d.price if d.price else 0),
        reverse=True,
    )

    posts: list[dict] = []
    for d in ranked[:limit]:
        margin_pct = round((d.price - d.cost) / d.price * 100) if d.price else 0
        posts.append(
            {
                "emoji": _emoji_for(d.name),
                "title": f"Hero the {d.name.lower()}",
                "rationale": (
                    f"{margin_pct}% margin — one of your most profitable items. "
                    "Make it the star of a post and a set-meal anchor."
                ),
                "caption": _caption(d.name, shop_name),
            }
        )

    # Always add a bundle idea built on the top two heroes.
    if len(ranked) >= 2:
        a, b = ranked[0], ranked[1]
        bundle_price = round((a.price + b.price) * 0.82)
        posts.append(
            {
                "emoji": "🫖",
                "title": "Weekday afternoon-tea set",
                "rationale": (
                    f"Bundle {a.name} + {b.name} at HK${bundle_price}. Raises ticket size "
                    "on your highest-margin items during the slow afternoon."
                ),
                "caption": (
                    f"Afternoon slump? {a.name} + {b.name} for HK${bundle_price}, "
                    f"weekdays 2-5pm at {shop_name}. #AfternoonTea #SetMenu"
                ),
            }
        )

    provider = get_provider()
    if provider.name != "mock":
        try:
            extra = provider.complete(
                f"Write one more Instagram caption for {shop_name}'s {ranked[0].name} "
                "aimed at local office workers.",
                system="You are a HK food social-media copywriter.",
            )
            posts.append(
                {
                    "emoji": "📸",
                    "title": "Behind the counter",
                    "rationale": "People buy stories. Show the kitchen, the regulars, the neighbourhood.",
                    "caption": extra,
                }
            )
        except Exception:  # pragma: no cover - network path
            pass

    return posts
