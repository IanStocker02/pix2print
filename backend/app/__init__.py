from fastapi import FastAPI

app = FastAPI()

from .auth.routes import router as auth_router

app.include_router(auth_router)