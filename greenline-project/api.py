from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from carbon_service import get_carbon_intensity
from ai_service import run_green_ai

app = FastAPI(title="GREENLINE API")

# 👇 ADD THIS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hackathon-safe
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/run")
def run_greenline(req: PromptRequest):
    intensity = get_carbon_intensity()
    response, mode = run_green_ai(req.prompt, intensity)

    return {
        "carbon_intensity": intensity,
        "mode": mode,
        "response": response
    }
