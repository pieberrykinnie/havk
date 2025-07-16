from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AnimationRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"message": "HAVK AI Animation Backend"}

@app.post("/animate")
def animate(req: AnimationRequest):
    # Placeholder for AI animation logic
    return {"animation_url": "https://example.com/animation.mp4", "prompt": req.prompt}