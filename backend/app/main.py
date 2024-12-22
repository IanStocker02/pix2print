from fastapi import FastAPI
from app.auth.routes import auth_router

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the JWT Authentication API"}