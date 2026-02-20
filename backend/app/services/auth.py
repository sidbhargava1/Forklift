import time
from typing import Any

import httpx
from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.core.config import get_settings


class Auth0Verifier:
    def __init__(self) -> None:
        self._jwks: dict[str, Any] | None = None
        self._jwks_cached_at: float = 0
        self._jwks_cache_ttl_seconds = 3600

    async def _fetch_jwks(self) -> dict[str, Any]:
        settings = get_settings()
        if not settings.auth0_domain:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Auth0 domain is not configured.",
            )

        now = time.time()
        if self._jwks and now - self._jwks_cached_at < self._jwks_cache_ttl_seconds:
            return self._jwks

        jwks_url = f"https://{settings.auth0_domain}/.well-known/jwks.json"
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(jwks_url)
            response.raise_for_status()
            self._jwks = response.json()
            self._jwks_cached_at = now
            return self._jwks

    async def verify_token(self, token: str) -> dict[str, Any]:
        settings = get_settings()

        if not settings.auth0_audience or not settings.auth0_issuer:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Auth0 audience/issuer are not configured.",
            )

        try:
            unverified_header = jwt.get_unverified_header(token)
            jwks = await self._fetch_jwks()
            rsa_key = {}
            for key in jwks.get("keys", []):
                if key.get("kid") == unverified_header.get("kid"):
                    rsa_key = {
                        "kty": key.get("kty"),
                        "kid": key.get("kid"),
                        "use": key.get("use"),
                        "n": key.get("n"),
                        "e": key.get("e"),
                    }
                    break

            if not rsa_key:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unable to find matching JWKS key.",
                )

            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=settings.auth0_audience,
                issuer=settings.auth0_issuer,
            )
            return payload
        except JWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token.",
            ) from exc


auth0_verifier = Auth0Verifier()
