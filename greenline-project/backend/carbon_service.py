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
        response.raise_for_status()
        data = response.json()
        
        
        actual_intensity = data['data'][0]['intensity']['actual']
        
        #forecast as backup
        if actual_intensity is None:
            actual_intensity = data['data'][0]['intensity']['forecast']
            
        return actual_intensity
    except Exception as e:
        print(f"⚠️ Error fetching carbon data: {e}")
        return 500  # default to high intensity if API fails
