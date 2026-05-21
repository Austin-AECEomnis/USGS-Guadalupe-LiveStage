pythonimport requests
import json
from datetime import datetime

# USGS gauge site number for Guadalupe River at Hunt, TX
SITE_NUMBER = "08165500"

# USGS Water Services API URL
URL = f"https://waterservices.usgs.gov/nwis/iv/?sites={SITE_NUMBER}&parameterCd=00065&format=json"

def fetch_stage():
    response = requests.get(URL)
    data = response.json()
    
    # Pull the most recent stage reading
    time_series = data["value"]["timeSeries"][0]
    latest = time_series["values"][0]["value"][0]
    
    stage_ft = latest["value"]
    timestamp = latest["dateTime"]
    
    # Format timestamp for display
    dt = datetime.fromisoformat(timestamp[:-6])
    formatted_time = dt.strftime("%m/%d/%Y %I:%M %p")
    
    result = {
        "stage_ft": stage_ft,
        "timestamp": formatted_time,
        "site": "Guadalupe River at Hunt, TX"
    }
    
    print(json.dumps(result, indent=2))
    
    # Save to file for Experience Builder to read
    with open("current_stage.json", "w") as f:
        json.dump(result, f, indent=2)

fetch_stage()
