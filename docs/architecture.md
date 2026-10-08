# ShopDoctor — Architecture & Design Notes

## Overview

ShopDoctor is a three-tier application:

1. **Frontend** — React 18 + Vite + TypeScript SPA. Talks to the backend through
   a single typed API client (`src/api/client.ts`). In dev, Vite proxies `/api`
   to the FastAPI server so there are no CORS issues.
2. **Backend** — FastAPI + SQLAlchemy 2.0 over SQLite. Thin routers delegate all
   reasoning to the agent layer; a `services.py` module orchestrates agents into
   a full report.
3. **AI agents** — a package of single-purpose agents behind a common
   `LLMProvider` interface.

```
Browser (React SPA)
   │  fetch /api/...
   ▼
FastAPI routers ──► services.build_report()
   │                      │
   │                      ├─ twin_shop_agent  (benchmark survivors vs closed)
   │                      ├─ diagnosis_agent  (score, margins, problems)
   │                      └─ LLMProvider.complete()  (optional narrative polish)
   ▼
SQLite (Shop, Dish, TwinShop)
```

## The provider seam (offline-first AI)

`app/agents/base.py` defines:

```python
class LLMProvider(ABC):
    def complete(self, prompt: str, *, system: str | None = None) -> str: ...
```

Three implementations:

- **`MockProvider`** (default) — returns a deterministic string. No network, no
  key. The whole app is fully functional offline.
- **`OpenAIProvider`** — chat-completions over `httpx`.
- **`AnthropicProvider`** — messages API over `httpx`.

`get_provider()` reads config and returns the right one; if a real provider is
requested but its key is missing, it **falls back to mock** so the app never
breaks. Agents call `provider.complete(...)` only for *optional* natural-language
polish and wrap it in `try/except`, so a network failure degrades gracefully.

**Key design decision:** all quantitative reasoning — the health score, dish
margins, the elasticity simulator, and chat intent detection — is **deterministic
Python**, not model output. This makes the demo reproducible, explainable to
shop owners ("why is my score 54?"), and unit-testable without mocking an LLM.
The model is a layer on top, not the foundation.

## Agents

| Agent | Responsibility | Deterministic? |
|-------|----------------|----------------|
| `diagnosis_agent` | Health Score, per-dish margins/status, ranked problems, written diagnosis | Yes (optional LLM polish) |
| `twin_shop_agent` | Group benchmark shops into survivors/closed; compute comparative stats | Yes |
| `pricing_agent` | Price → demand → profit simulation via elasticity | Yes |
| `chat_agent` | Bilingual (EN/廣東話) intent detection + grounded replies | Yes (optional LLM reply) |
| `marketing_agent` | Rank dishes by margin → post ideas, captions, photo briefs | Yes (optional LLM caption) |

### Health Score

Weighted sum of five band-scored components (see README for weights and
thresholds). `_band_score(value, good, bad)` maps a metric linearly to 0–100
between its healthy and unhealthy thresholds. Problems are emitted by rule
(losing dishes, thin high-share sellers, high waste vs survivors, high rent
ratio, under-promoted stars), so each one is traceable to the data.

### Twin Shops

The "diagnosis by comparison" idea from the pitch: similar shops are split into
**Survivors** (still open after 2 years) and **Closed**. `benchmark_stats()`
averages margin/waste/menu-size across each group; the diagnosis positions the
owner's shop relative to both. Seeded with an illustrative dataset of cha chaan
tengs in Kowloon.

### Price Simulator

```
units(new_price) = base_units * (new_price / base_price) ** elasticity
profit = (price - cost) * units
```

Default elasticity `-1.4` (configurable). Advice buckets the profit delta into
up / down / flat with a plain-language recommendation.

### Chat

`detect_intent()` matches regex intents (margin, price, waste, marketing, score,
greet) across English and Cantonese keywords. Offline, curated bilingual answers
are returned; with a real provider, the report text is passed as context and the
model answers in the requested language.

## Data model

- **Shop** — profile, opening hours, and monthly financials (revenue, rent,
  staff cost, ingredient %, waste %, menu size).
- **Dish** — belongs to a shop; price, cost, units/month, share%.
- **TwinShop** — benchmark record (name, outcome survived/closed, trait, avg
  margin, waste, menu size). Not owned by a shop; used for comparison.

SQLite by default for zero-setup local runs; swap `DATABASE_URL` for Postgres in
production (SQLAlchemy makes this a config change).

## API contract & typing

Pydantic schemas (`backend/app/schemas.py`) are the single source of truth for
request/response shapes. The frontend `types.ts` mirrors them, and `api/client.ts`
is fully typed, so contract drift surfaces as a TypeScript error.

## Testing & CI

- **Backend:** pytest with an in-memory/temp SQLite DB and the mock provider.
  Covers health, report structure & scoring, dish-margin math, twin groups,
  404s, and shop creation → diagnosis.
- **Frontend:** `tsc` typecheck + production build.
- **CI:** GitHub Actions runs both on every push/PR to `main`.

## Extending

- **Real OCR of menu photos** — replace the stubbed upload step with a vision
  model behind the same provider interface; emit `Dish` rows.
- **Auth / multi-tenant** — add an owner account model and scope shops to it.
- **Real twin-shop data** — back the benchmark from a scraped/licensed dataset
  of HK business registrations instead of the seed.
- **Persistence of reports** — currently computed on demand; cache snapshots to
  power the month-over-month "follow-up" that the Pro tier promises.
