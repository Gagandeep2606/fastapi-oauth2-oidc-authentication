# OAuth and ODIC configuration

from authlib.integrations.starlette_client import OAuth
from core.config import GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET

import secrets

oauth = OAuth()

oauth.register(
    name= "google",
    client_id = GOOGLE_CLIENT_ID,
    client_secret = GOOGLE_CLIENT_SECRET,
    server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs = {
        "scope": "openid email profile"
    }
)


def generate_refresh_token():
    return secrets.token_urlsafe(64)