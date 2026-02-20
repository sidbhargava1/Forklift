from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings
from app.services.auth import auth0_verifier

bearer_scheme = HTTPBearer(auto_error=False)
credentials_dependency = Depends(bearer_scheme)


async def get_current_user_claims(
    credentials: HTTPAuthorizationCredentials | None = credentials_dependency,
) -> dict[str, Any]:
    settings = get_settings()

    if not settings.auth_enabled:
        return {"sub": "dev-user", "auth_enabled": False}

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )

    return await auth0_verifier.verify_token(credentials.credentials)
