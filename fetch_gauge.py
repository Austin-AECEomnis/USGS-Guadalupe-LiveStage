import requests
import json
from datetime import datetime

SITE_NUMBER = "08165500"
URL = f"https://waterservices.usgs.gov/nwis/iv/?sites={SITE_NUMBER}&parameterCd=00065&format=json&period=PT2H"

def fetch_stage():
    headers = {"Cache-Control": "no-cache", "Pragma": "no-cache"}
    response = requests.get(URL, headers=headers)
    data = response.json()

    time_series = data["value"]["timeSeries"][0]
    latest = time_series["values"][0]["value"][-1]
    stage_ft = latest["value"]
    timestamp = latest["dateTime"]

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
