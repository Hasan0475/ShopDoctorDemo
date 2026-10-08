"""ShopDoctor API — FastAPI application entrypoint."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import init_db
from .routers import chat, health, marketing, report, shops, simulator
from .seed import seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed()  # no-op once data exists
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=(
        "An AI business check-up for Hong Kong's small shops. Free diagnosis, "
        "paid follow-up care. Built for HACK4SDG (SDG 8)."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API = "/api"
app.include_router(health.router, prefix=API)
app.include_router(shops.router, prefix=API)
app.include_router(report.router, prefix=API)
app.include_router(simulator.router, prefix=API)
app.include_router(chat.router, prefix=API)
app.include_router(marketing.router, prefix=API)


@app.get("/", tags=["health"])
def root():
    return {
        "app": settings.app_name,
        "version": settings.version,
        "docs": "/docs",
        "health": f"{API}/health",
    }
