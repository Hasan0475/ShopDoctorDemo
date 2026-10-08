"""Health / meta endpoint."""
from __future__ import annotations

from fastapi import APIRouter

from ..agents import get_provider
from ..config import settings
from ..schemas import HealthOut

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthOut)
def health() -> HealthOut:
    return HealthOut(status="ok", version=settings.version, llm_provider=get_provider().name)
