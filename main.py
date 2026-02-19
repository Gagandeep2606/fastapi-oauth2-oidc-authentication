
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from auth.google import router as auth_route
from auth.profile import router as profile_router
from models.user import router as user_router

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
     secret_key="random_session_secret"
)

app.include_router(auth_route)
app.include_router(profile_router)
app.include_router(user_router)

@app.get("/")
def home():
    return{"status":"App running"}

   


