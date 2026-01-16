from carbon_service import get_carbon_intensity
from ai_service import run_green_ai

def main():
    print("--- 🟢 GREENLINE MIDDLEWARE ACTIVATED ---")
    user_prompt = input("Enter your AI request: ")
    
    # Step 1: Query the National Grid
    print("📡 Querying National Grid for carbon intensity...")
    intensity = get_carbon_intensity()
    print(f"📊 Current Intensity: {intensity} gCO2/kWh")
    
    # Step 2: Route the request
    result, mode_info = run_green_ai(user_prompt, intensity)
    
    # Step 3: Display results
    print("\n" + "="*40)
    print(f"ROUTING STATUS: {mode_info}")
    print("-" * 40)
    print(f"GROQ SAYS: {result}")
    print("="*40)

if __name__ == "__main__":
    main()