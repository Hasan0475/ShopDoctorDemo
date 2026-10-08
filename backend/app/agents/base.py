"""LLM provider abstraction.

ShopDoctor's agents talk to a provider through one tiny interface so the whole
app runs offline by default (``MockProvider``) and can be switched to a real
model by config alone. To go live:

    LLM_PROVIDER=openai OPENAI_API_KEY=sk-...    (or)
    LLM_PROVIDER=anthropic ANTHROPIC_API_KEY=sk-ant-...

No agent code changes — they only ever call ``get_provider().complete(...)``.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

import httpx

from ..config import settings


class LLMProvider(ABC):
    """Minimal interface every provider implements."""

    name: str = "base"

    @abstractmethod
    def complete(self, prompt: str, *, system: str | None = None) -> str:
        """Return a text completion for ``prompt``."""

    def available(self) -> bool:
        return True


class MockProvider(LLMProvider):
    """Deterministic, offline provider.

    Agents embed their own domain logic and use the provider only for optional
    natural-language polish, so the mock returns a stable, sensible string and
    never blocks the deterministic pipeline.
    """

    name = "mock"

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        # Echo a short, deterministic acknowledgement. Real narrative is
        # produced by the agents themselves, so the demo never looks empty.
        first_line = prompt.strip().splitlines()[0][:80] if prompt.strip() else ""
        return f"[mock-llm] {first_line}".strip()


class OpenAIProvider(LLMProvider):
    """Real-ready OpenAI chat-completions provider."""

    name = "openai"

    def __init__(self, api_key: str, model: str, timeout: float) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        resp = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": self.model, "messages": messages, "temperature": 0.4},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


class AnthropicProvider(LLMProvider):
    """Real-ready Anthropic messages provider."""

    name = "anthropic"

    def __init__(self, api_key: str, model: str, timeout: float) -> None:
        self.api_key = api_key
        self.model = model or "claude-3-5-haiku-latest"
        self.timeout = timeout

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        body: dict = {
            "model": self.model,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            body["system"] = system
        resp = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json=body,
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()["content"][0]["text"]


_provider: LLMProvider | None = None


def get_provider() -> LLMProvider:
    """Return the configured provider (cached). Falls back to mock if a real
    provider is requested but its API key is missing, so the app always runs."""
    global _provider
    if _provider is not None:
        return _provider

    kind = (settings.llm_provider or "mock").lower()
    if kind == "openai" and settings.openai_api_key:
        _provider = OpenAIProvider(settings.openai_api_key, settings.llm_model, settings.llm_timeout)
    elif kind == "anthropic" and settings.anthropic_api_key:
        _provider = AnthropicProvider(settings.anthropic_api_key, settings.llm_model, settings.llm_timeout)
    else:
        _provider = MockProvider()
    return _provider


def reset_provider() -> None:
    """Clear the cached provider (used in tests)."""
    global _provider
    _provider = None
