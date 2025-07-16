from fastapi import FastAPI

app = FastAPI(title="HAVK Scarcity Solution API")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Hello, HAVK!"}