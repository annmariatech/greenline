import requests

def get_carbon_intensity():
    """
    Fetches real-time carbon intensity from the National Grid API.
    Returns: The 'actual' carbon intensity value (gCO2/kWh).
    """
    url = "https://api.carbonintensity.org.uk/intensity"
    headers = {"Accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Check for errors
        data = response.json()
        
        # Extract the 'actual' intensity from the JSON response
        actual_intensity = data['data'][0]['intensity']['actual']
        
        # If 'actual' is missing (can happen), use 'forecast'
        if actual_intensity is None:
            actual_intensity = data['data'][0]['intensity']['forecast']
            
        return actual_intensity
    except Exception as e:
        print(f"⚠️ Error fetching carbon data: {e}")
        return 500  # Default to 'High' intensity if API fails (safety first!)