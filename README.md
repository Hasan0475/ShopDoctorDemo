# ShopDoctor 🩺

**An AI business check-up for Hong Kong's small shops.** Built for **HACK4SDG** —
Track 4: Future Work &amp; Enterprises · **SDG 8: Decent Work &amp; Economic Growth**.

Shop Doctor reads a restaurant's numbers, finds what is losing money, and gives
data-backed suggestions — like a family doctor for small shops. A 20-minute
check-up produces a **Health Score**, per-dish **profit margins**, a **Twin Shops**
benchmark (survivors vs closed), a **Price Simulator**, a bilingual **Ask Shop
Doctor** chat (English / 廣東話), and a **Marketing Kit**.

> Free check-up brings owners in; Pro follow-up care (HK$999/mo) is the revenue.

---

## ✨ Features

| Tool | What it does |
|------|--------------|
| **Health Report** | Health Score (0–100), net-margin & prediction metrics, per-dish margins, ranked problems |
| **Twin Shops** | Finds similar nearby shops, splits them into *Survivors* (open after 2 yrs) and *Closed*, and diagnoses the difference |
| **Price Simulator** | Slide a dish price → see monthly profit change, using a demand elasticity estimated from twin-shop data |
| **Ask Shop Doctor** | Follow-up chat in **Cantonese or English**, grounded in the shop's report |
| **Marketing Kit** | Instagram post ideas, captions & photo briefs that favour the highest-margin dishes |
| **Check-Up wizard** | 5-step intake: shop basics → photos/listing → hours → revenue & costs → menu |

---

## 🏗️ Architecture

A three-tier monorepo. The AI layer sits behind a **provider interface** so the
whole app runs **fully offline by default** (deterministic mock agents) and can
switch to a real model by config alone — no code changes.

```
shopdoctor/
├── backend/                 FastAPI + SQLAlchemy (SQLite)
│   ├── app/
│   │   ├── main.py          App entrypoint, CORS, router wiring, lifespan seed
│   │   ├── config.py        Pydantic settings (env-driven)
│   │   ├── database.py      Engine / session / Base
│   │   ├── models.py        Shop, Dish, TwinShop
│   │   ├── schemas.py       Pydantic request/response contracts
│   │   ├── crud.py          DB helpers
│   │   ├── seed.py          Demo shop + twin-shop benchmark dataset
│   │   ├── services.py      Report orchestration
│   │   ├── routers/         health, shops, report, simulator, chat, marketing
│   │   └── agents/          ★ the AI layer
│   │       ├── base.py             LLMProvider interface (mock / OpenAI / Anthropic)
│   │       ├── diagnosis_agent.py  Health score, margins, problems, narrative
│   │       ├── twin_shop_agent.py  Survivor vs closed benchmarking
│   │       ├── pricing_agent.py    Deterministic elasticity simulator
│   │       ├── chat_agent.py       Bilingual intent + grounded replies
│   │       └── marketing_agent.py  Post/caption generation
│   └── tests/               pytest suite
├── frontend/                React 18 + Vite + TypeScript
│   └── src/
│       ├── api/client.ts    Typed API client
│       ├── types.ts         Contracts mirroring the backend
│       ├── components/      ShopContext, ui primitives
│       └── pages/           Home, CheckUp, HealthReport, Simulator, Chat, Marketing, Business
├── docs/architecture.md     Deeper design notes
├── docker-compose.yml       One-command full stack
└── .github/workflows/ci.yml Backend tests + frontend typecheck/build
```

### The agent → provider seam

Every agent calls `get_provider().complete(...)` for optional natural-language
polish. The **deterministic domain logic (scores, margins, elasticity, intent
detection) never depends on a model**, so results are stable, explainable and
testable offline. Drop in a key to make the narrative model-generated:

```bash
LLM_PROVIDER=openai   OPENAI_API_KEY=sk-...     # or
LLM_PROVIDER=anthropic ANTHROPIC_API_KEY=sk-ant-...
```

See [`docs/architecture.md`](docs/architecture.md) for the full design.

---

## 🚀 Quick start

### Option A — Docker (whole stack, one command)

```bash
docker compose up --build
# frontend → http://localhost:8080   backend/API docs → http://localhost:8000/docs
```

### Option B — Local dev (hot reload)

**Backend** (Python 3.11+):

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend** (Node 18+):

```bash
cd frontend
npm install
npm run dev                       # http://localhost:5173 (proxies /api → :8000)
```

The database seeds itself on first boot with a demo shop (**Ming Kee Cha Chaan
Teng**) and the twin-shop benchmark dataset.

### Tests

```bash
cd backend && pytest -q           # 6 passing: health, report scoring, twins, shop creation
cd frontend && npm run typecheck && npm run build
```

---

## 🔌 API

Base path `/api`. Interactive docs at `http://localhost:8000/docs`.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Service status + active LLM provider |
| GET | `/api/shops` | List shops |
| POST | `/api/shops` | Create a shop (check-up submission) |
| GET | `/api/shops/{id}` | Shop details |
| GET | `/api/shops/{id}/report` | Full Health Report (diagnosis) |
| GET | `/api/shops/{id}/twins` | Survivor vs closed benchmark groups |
| GET | `/api/shops/meta/benchmark` | Twin-shop aggregate stats |
| POST | `/api/simulator` | Price → profit simulation |
| POST | `/api/chat` | Bilingual Ask Shop Doctor |
| GET | `/api/shops/{id}/marketing` | Marketing Kit posts |

---

## 🧮 How the Health Score works

A transparent, weighted 0–100 score (no black box):

- **30%** average dish margin — benchmarked `MARGIN_BAD…MARGIN_GOOD` (32%→58%)
- **20%** rent / revenue — healthy ≤ 22%, bad ≥ 38%
- **18%** labour / revenue — healthy ≤ 25%, bad ≥ 42%
- **17%** COGS ratio — healthy ≤ 28%, bad ≥ 40%
- **15%** food waste — healthy ≤ 4%, bad ≥ 11%

Bands: **≥75 healthy · 60–74 watch · <60 at-risk**. Each component is scored
linearly between its good/bad thresholds, so owners can see exactly what moves
the needle.

---

## 🗺️ Roadmap

Hackathon prototype (Oct 2026) → Pilot with 10+ owners (Nov 2026–Mar 2027) →
Launch, Pro tier live, 100+ shops (Apr–Sep 2027) → Scale to 1,000+ shops (2028+).

## 📄 License

MIT — see [LICENSE](LICENSE). All figures in this demo are illustrative.
