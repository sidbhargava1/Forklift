from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "environment": settings.environment,
        "service": "backend",
    }


@router.get("/integrations")
def integrations_status() -> dict[str, bool]:
    settings = get_settings()
    return {
        "openai_configured": bool(settings.openai_api_key),
        "redis_configured": bool(settings.redis_url),
        "auth_enabled": settings.auth_enabled,
    }
