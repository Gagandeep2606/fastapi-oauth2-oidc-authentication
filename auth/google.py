from fastapi import APIRouter, Request
from core.security import oauth
from core.jwt import create_access_token
from datetime import datetime,timedelta
from core.database import collection,refresh_tokens_collection

router = APIRouter(prefix="/auth/google", tags=["Google OAuth"])

@router.get("/login")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback", name="google_callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.userinfo(token=token)

    email = user_info["email"]

    user = collection.find_one({"email": email})

    if not user:
        user = {
            "email": email,
            "name": user_info.get("name"),
            "provider": "google",
            "google_id": user_info["sub"],
            "created_at": datetime.utcnow()
        }
        result = collection.insert_one(user)
        user["_id"] = result.inserted_id

    access_token = create_access_token(
        data={
            "sub": str(user["_id"]),
            "email": user["email"],
            "name": user.get("name"),
            "provider": user["provider"]
        }
    )

    refresh_token = create_access_token(
        data={
            "sub": str(user["_id"]),
            "exp": datetime.utcnow() + timedelta(days=7)
        }
    )

    refresh_tokens_collection.insert_one({
    "user_id": user["_id"],
    "token": refresh_token,
    "expires_at": datetime.utcnow() + timedelta(days=7),
    "revoked": False,
    "created_at": datetime.utcnow()
})

    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token":refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(refresh_token: str):
    refresh_tokens_collection.update_one(
        {"token": refresh_token},
        {"$set": {"revoked": True}}
    )
    return {"message": "Logged out"}

