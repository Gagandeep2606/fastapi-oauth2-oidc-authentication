from fastapi import APIRouter, Depends
from core.dependencies import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/")
async def profile(current_user=Depends(get_current_user)):
    return {
        "message": "Protected route access granted",
        "user": current_user
    }
