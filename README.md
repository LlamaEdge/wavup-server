# WavUp Service

This service converts audio files (e.g., OGG, FLAC, OPUS) to 16kHz WAV format.

## Setup

- Install dependencies

```bash
# Optional: use conda or other tools to create a new virtual environment
conda create -n wavup python=3.11
conda activate wavup

# Install dependencies
pip install -r requirements.txt
```

- Install ffmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt-get install ffmpeg
```

## Run

```bash
# run on default port (9069)
python server.py

# run on custom port
python server.py --port 9069
```

## Test

- Test with `curl`

```bash
# First, convert audio file to base64
BASE64_AUDIO=$(base64 -w 0 input.ogg)

# Send request
curl -X POST \
     -H "Content-Type: application/json" \
     -d "{\"contents\":\"$BASE64_AUDIO\"}" \
     http://localhost:9069/convert > response.json

# Extract and decode audio data from response
cat response.json | jq -r '.contents' | base64 -d > output.wav
```

- Test with `python`

```bash
cd test
python client.py
```

If the Python script runs successfully, you should see the output file `output.wav` in the `test` directory.
