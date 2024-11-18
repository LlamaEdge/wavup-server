import argparse
import base64
import io
import json
import os
import tempfile

from flask import Flask, make_response, request
from pydub import AudioSegment

app = Flask(__name__)

TARGET_SAMPLE_RATE = 16000  # 16kHz


@app.route("/convert", methods=["POST"])
def convert_audio():
    try:
        # Check if request has JSON data
        if not request.is_json:
            return {"error": "Request must be JSON"}, 400

        data = request.get_json()

        # Check if 'contents' field exists
        if "contents" not in data:
            return {"error": "Missing contents field"}, 400

        try:
            # Decode base64 audio data
            audio_bytes = base64.b64decode(data["contents"])

            # Create memory buffer for input data
            audio_buffer = io.BytesIO(audio_bytes)

            # Try to load the audio data
            # pydub will automatically detect the codec (vorbis, FLAC, opus)
            audio = AudioSegment.from_file(audio_buffer, format="ogg")

            # Resample to 16kHz if necessary
            if audio.frame_rate != TARGET_SAMPLE_RATE:
                audio = audio.set_frame_rate(TARGET_SAMPLE_RATE)

            # Create memory buffer for WAV output
            wav_buffer = io.BytesIO()

            # Export to WAV format
            # Set parameters for 16kHz WAV
            audio.export(
                wav_buffer,
                format="wav",
                parameters=[
                    "-ar",
                    str(TARGET_SAMPLE_RATE),  # Set audio rate
                ],
            )

            # Get the bytes from the buffer and encode as base64
            wav_bytes = base64.b64encode(wav_buffer.getvalue()).decode("utf-8")

            # Return JSON response with wav bytes
            return {"contents": wav_bytes}

        except Exception as e:
            return {"error": f"Audio conversion failed: {str(e)}"}, 500

    except Exception as e:
        return {"error": f"Request processing failed: {str(e)}"}, 500


def parse_args():
    parser = argparse.ArgumentParser(description="Audio conversion server")
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=9069,
        help="Port to run the server on (default: 9069)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    app.run(host="0.0.0.0", port=args.port)