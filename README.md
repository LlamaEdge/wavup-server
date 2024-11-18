# WavUp Service

This service converts audio files (e.g., Vorbis, FLAC, Opus encoded Ogg/Oga audio files) to 16kHz WAV format.

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
# 发送请求
curl -X POST --data-binary @input.ogg \
  -H "Content-Type: audio/ogg" \
  http://localhost:9069/convert \
  --output output.wav
```

- Test with `python`

```bash
cd test
python client.py
```

If the Python script runs successfully, you should see the output file `output.wav` in the `test` directory.
