from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user_claims

router = APIRouter(prefix="/auth", tags=["auth"])
current_user_claims_dependency = Depends(get_current_user_claims)


@router.get("/me")
async def get_me(claims: dict[str, Any] = current_user_claims_dependency) -> dict[str, Any]:
    return {"claims": claims}
