import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_CONFIG = {
    "llama-3.1-8b-instant": {
        "params_billion": 8,
        "energy_kwh": 0.002 #assumed
    },
    "llama-3.3-70b-versatile": {
        "params_billion": 70,
        "energy_kwh": 0.015 #assumed
    }
}

BASELINE_MODEL = "llama-3.3-70b-versatile"

def run_green_ai(prompt, carbon_score, remaining_budget=None):
    if carbon_score > 200:
        model = "llama-3.1-8b-instant"
        mode = "🌿 ECO-MODE (Low Power Model)"
    else:
        model = "llama-3.3-70b-versatile"
        mode = "⚡ PERFORMANCE-MODE (High Power Model)"

    eco_cost = MODEL_CONFIG["llama-3.1-8b-instant"]["energy_kwh"] * carbon_score
    perf_cost = MODEL_CONFIG["llama-3.3-70b-versatile"]["energy_kwh"] * carbon_score

    if remaining_budget is not None and remaining_budget < perf_cost:
        model = "llama-3.1-8b-instant"
        mode = "🌿 ECO-MODE (Budget Enforced)"
        # also shorten response implicitly via prompt
        prompt = f"Answer concisely:\n{prompt}"

    elif carbon_score > 200:
        model = "llama-3.1-8b-instant"
        mode = "🌿 ECO-MODE (Low Power)"


    try:
        
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            timeout=20
        )

        ai_text = completion.choices[0].message.content

        
        energy_used = MODEL_CONFIG[model]["energy_kwh"]
        carbon_spent = energy_used * carbon_score

        baseline_energy = MODEL_CONFIG[BASELINE_MODEL]["energy_kwh"]

        
        co2_emitted = energy_used * carbon_score
        baseline_co2 = baseline_energy * carbon_score
        carbon_saved = baseline_co2 - co2_emitted

        return {
            "response": ai_text,
            "mode": mode,
            "carbon_spent": round(carbon_spent, 2),
            "carbon_receipt": {
                "model": model,
                "energy_kwh": round(energy_used, 5),
                "co2_grams": round(co2_emitted, 2),
                "baseline_co2_grams": round(baseline_co2, 2),
                "carbon_saved_grams": round(carbon_saved, 2),
            }
        }

    except Exception as e:
        print("❌ Groq API Error:", e)
        return {
            "response": "AI request failed.",
            "mode": "⚠️ ERROR",
            "carbon_receipt": None
        }

