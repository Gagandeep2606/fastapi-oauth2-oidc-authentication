from fastapi import APIRouter
from core.database import refresh_tokens_collection

router = APIRouter()

@router.post("/auth/logout")
def logout(refresh_token: str):
    refresh_tokens_collection.update_one(
        {"token": refresh_token},
        {"$set": {"revoked": True}}
    )

    return {"message": "Logged out successfully"}
