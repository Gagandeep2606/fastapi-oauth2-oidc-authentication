
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from auth.route import router as auth_route


app = FastAPI()

app.add_middleware(
    SessionMiddleware,
     secret_key="random_session_secret"
)

app.include_router(auth_route)

@app.get("/")
def home():
    return{"status":"App running"}
