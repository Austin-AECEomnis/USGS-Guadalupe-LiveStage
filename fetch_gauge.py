import requests
import json
from datetime import datetime

SITE_NUMBER = "08165500"
URL = f"https://api.waterdata.usgs.gov/observations/monitoring-locations/{SITE_NUMBER}/observations?parameterCode=00065&period=PT2H&format=json"

def fetch_stage():
    response = requests.get(URL)
    data = response.json()

    observations = data["features"][0]["properties"]["observations"]
    latest = observations[-1]
    stage_ft = latest["result"]
    timestamp = latest["phenomenonTime"]

    dt = datetime.fromisoformat(timestamp[:-6])
    formatted_time = dt.strftime("%m/%d/%Y %I:%M %p")

    result = {
        "stage_ft": stage_ft,
        "timestamp": formatted_time,
        "site": "Guadalupe River at Hunt, TX"
    }

    print(json.dumps(result, indent=2))

    with open("current_stage.json", "w") as f:
        json.dump(result, f, indent=2)

fetch_stage()
