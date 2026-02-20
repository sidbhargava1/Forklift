import hashlib
import json
from typing import Any

import redis.asyncio as redis
from openai import AsyncOpenAI

from app.core.config import get_settings
from app.services.prompt_loader import load_prompt


class LLMClient:
    """
    Generic OpenAI connector with optional Redis caching.

    Use from your own services/use cases, e.g.:
        await llm_client.generate(prompt_name="system", input_text="Hello")
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        self._redis_client: redis.Redis | None = None
        self._openai_client: AsyncOpenAI | None = None

        if self.settings.openai_api_key:
            self._openai_client = AsyncOpenAI(api_key=self.settings.openai_api_key)

    async def _get_redis(self) -> redis.Redis:
        if self._redis_client is None:
            self._redis_client = redis.from_url(self.settings.redis_url, decode_responses=True)
        return self._redis_client

    async def _get_cache(self, key: str) -> dict[str, Any] | None:
        if not self.settings.llm_cache_enabled:
            return None

        try:
            client = await self._get_redis()
            cached = await client.get(key)
            if cached:
                return json.loads(cached)
        except Exception:
            return None

        return None

    async def _set_cache(self, key: str, payload: dict[str, Any]) -> None:
        if not self.settings.llm_cache_enabled:
            return

        try:
            client = await self._get_redis()
            await client.set(
                key,
                json.dumps(payload),
                ex=self.settings.openai_cache_ttl_seconds,
            )
        except Exception:
            return

    def _cache_key(self, prompt_name: str, prompt_text: str, input_text: str) -> str:
        digest_input = f"{self.settings.openai_model}:{prompt_name}:{prompt_text}:{input_text}".encode(
            "utf-8"
        )
        digest = hashlib.sha256(digest_input).hexdigest()
        return f"llm:completion:{digest}"

    async def generate(self, prompt_name: str, input_text: str) -> dict[str, Any]:
        prompt_text = load_prompt(prompt_name)
        cache_key = self._cache_key(prompt_name=prompt_name, prompt_text=prompt_text, input_text=input_text)

        cached = await self._get_cache(cache_key)
        if cached:
            return {
                "output_text": cached["output_text"],
                "model": cached["model"],
                "cached": True,
            }

        if not self._openai_client:
            return {
                "output_text": "OPENAI_API_KEY is not configured. Set it in .env to enable live LLM responses.",
                "model": "not-configured",
                "cached": False,
            }

        response = await self._openai_client.responses.create(
            model=self.settings.openai_model,
            input=[
                {"role": "system", "content": prompt_text},
                {"role": "user", "content": input_text},
            ],
        )

        result = {
            "output_text": response.output_text or "",
            "model": response.model,
            "cached": False,
        }

        await self._set_cache(cache_key, result)
        return result

    async def close(self) -> None:
        if self._redis_client is not None:
            await self._redis_client.aclose()
            self._redis_client = None


llm_client = LLMClient()
