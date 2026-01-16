import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_green_ai(prompt, carbon_score):
    # Carbon-aware routing
    if carbon_score > 200:
        model = "llama-3.1-8b-instant"   # eco mode
        mode = "🌿 ECO-MODE (Low Power Model)"
    else:
        model = "llama-3.3-70b-versatile"  # performance
        mode = "⚡ PERFORMANCE-MODE (High Power Model)"

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return completion.choices[0].message.content, mode

    except Exception as e:
        print("❌ Groq API Error:", e)
        return "AI request failed.", "⚠️ ERROR"
