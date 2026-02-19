from fastapi import APIRouter, HTTPException, status
from datetime import datetime,timedelta
from core.database import refresh_tokens_collection, collection
from core.jwt import verify_access_token, create_access_token
from bson import ObjectId

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/refresh")
def refresh_access_token(refresh_token: str):
    # 1️⃣ Verify refresh token JWT
    payload = verify_access_token(refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    user_id = payload.get("sub")

    # 2️⃣ Check refresh token in DB
    token_doc = refresh_tokens_collection.find_one({
        "token": refresh_token,
        "revoked": False
    })

    if not token_doc:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if token_doc["expires_at"] < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired")

    # 3️⃣ Load user
    user = collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 4️⃣ Issue new access token
    new_access_token = create_access_token(
        data={
            "sub": str(user["_id"]),
            "exp": datetime.utcnow() + timedelta(minutes=15)
        }
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

