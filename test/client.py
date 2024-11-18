import requests

# Read bytes from OGG file
with open("example_opus.oga", "rb") as f:
    ogg_bytes = f.read()

# Send request
response = requests.post(
    "http://localhost:9069/convert",
    data=ogg_bytes,
    headers={"Content-Type": "audio/ogg"},
)

if response.status_code == 200:
    # Save returned WAV bytes
    with open("output.wav", "wb") as f:
        f.write(response.content)
    print("Conversion successful")
else:
    print(f"Error: {response.json()}")
