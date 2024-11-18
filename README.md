# WavUp Service

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
python app.py

# run on custom port
python app.py --port 9069
```

## Test

```bash
curl -X POST -F "audio=@your_audio.ogg" http://localhost:9069/convert --output converted.wav
```
