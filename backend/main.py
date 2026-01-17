from carbon_service import get_carbon_intensity
from ai_service import run_green_ai

def main():
    print("--- 🟢 GREENLINE MIDDLEWARE ACTIVATED ---")
    user_prompt = input("Enter your AI request: ")


    print("📡 Querying National Grid for carbon intensity...")
    intensity = get_carbon_intensity()
    print(f"📊 Current Intensity: {intensity} gCO2/kWh")


    result = run_green_ai(user_prompt, intensity)

 
    print("\n" + "=" * 40)
    print(f"ROUTING STATUS: {result['mode']}")
    print("-" * 40)
    print(f"GROQ SAYS:\n{result['response']}")


    receipt = result.get("carbon_receipt")
    if receipt:
        print("\n🧾 CARBON RECEIPT")
        print(f"Model Used: {receipt['model']}")
        print(f"Energy Used: {receipt['energy_kwh']} kWh")
        print(f"CO₂ Emitted: {receipt['co2_grams']} g")
        print(f"Baseline CO₂: {receipt['baseline_co2_grams']} g")
        print(f"🌱 Carbon Saved: {receipt['carbon_saved_grams']} g")

    print("=" * 40)

if __name__ == "__main__":
    main()
