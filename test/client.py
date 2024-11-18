import base64
import json

import requests

# Read OGG file and convert to base64
with open("example_opus.oga", "rb") as f:
    ogg_bytes = base64.b64encode(f.read()).decode("utf-8")

# Prepare request data
request_data = {"contents": ogg_bytes}

# Send request
response = requests.post(
    "http://localhost:9069/convert",
    json=request_data,
    headers={"Content-Type": "application/json"},
)

if response.status_code == 200:
    # Get WAV data from response and decode
    wav_bytes = base64.b64decode(response.json()["contents"])

    # Save to file
    with open("output.wav", "wb") as f:
        f.write(wav_bytes)
    print("Conversion successful")
else:
    print(f"Error: {response.json()}")
