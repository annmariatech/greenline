from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from carbon_service import get_carbon_intensity
from ai_service import run_green_ai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)
class RunRequest(BaseModel):
    prompt: str
    budget: float | None = None
    used: float | None = None

@app.post("/run")
def run(req: RunRequest):
    intensity = get_carbon_intensity()

    remaining = None
    if req.budget is not None and req.used is not None:
        remaining = max(req.budget - req.used, 0)

    result = run_green_ai(req.prompt, intensity, remaining)

    new_used = (req.used or 0) + result.get("carbon_spent", 0)

    return {
        "carbon_intensity": intensity,
        "mode": result["mode"],
        "response": result["response"],
        "carbon_spent": result["carbon_spent"],
        "used": round(new_used, 2),
        "budget": req.budget,
        "carbon_receipt": result["carbon_receipt"]
    }
