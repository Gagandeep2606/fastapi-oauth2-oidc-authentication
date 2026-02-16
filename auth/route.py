from fastapi import APIRouter, Request
from core.security import oauth

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    print("Redirecting to:", redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback", name="auth_callback")
async def auth_callback(request: Request):

    #  Exchange code → tokens
    token = await oauth.google.authorize_access_token(request)

    # Verify ID token (OIDC step)
    user_info = await oauth.google.userinfo(token=token)

    return {
        "message": "Login successful",
        "email": user_info["email"],
        "name": user_info.get("name"),
        "google_id": user_info["sub"]
    }
