import argparse
import io
import os
import tempfile

from flask import Flask, request, send_file
from pydub import AudioSegment

app = Flask(__name__)

TARGET_SAMPLE_RATE = 16000  # 16kHz


@app.route("/convert", methods=["POST"])
def convert_audio():
    try:
        # Check if file is received
        if "audio" not in request.files:
            return {"error": "No audio file received"}, 400

        audio_file = request.files["audio"]

        # Check filename
        if audio_file.filename == "":
            return {"error": "Empty filename"}, 400

        # Create temporary file to save uploaded audio
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_input:
            audio_file.save(temp_input.name)

            try:
                # Try to load the audio file
                # pydub will automatically detect the codec (vorbis, FLAC, opus)
                audio = AudioSegment.from_file(temp_input.name)

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
                wav_buffer.seek(0)

                # Delete temporary file
                os.unlink(temp_input.name)

                # Return converted WAV file
                return send_file(
                    wav_buffer,
                    mimetype="audio/wav",
                    as_attachment=True,
                    download_name="converted.wav",
                )

            except Exception as e:
                # Delete temporary file
                os.unlink(temp_input.name)
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
