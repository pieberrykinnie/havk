from fastapi import FastAPI
import asyncio

from .api import auth
from .db.session import init_db

app = FastAPI(title="HAVK Scarcity Solution API")

# Register routers
app.include_router(auth.router)

# Initialize database on startup


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Hello, HAVK!"}