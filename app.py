from dataclasses import asdict
from flask import Flask, jsonify, request
from http import HTTPStatus

from app.services import TranscriptService
from db.mysql_repository import MySQLTranscriptRepository
from app.enums import ProcessingMode

app = Flask(__name__)

services = TranscriptService(MySQLTranscriptRepository())
@app.route("/")
def hello():
    return "Hello world!"

@app.route("/transcripts", methods=["POST"])
def create_transcript():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Request body must be valid JSON"}), HTTPStatus.BAD_REQUEST

    required_fields = ["podcast_name", "filename", "raw_transcription_text", "mode"]
    missing = [field_name for field_name in required_fields if field_name not in data]
    if missing:
        return jsonify({"error": f"Missing required field(s): {', '.join(missing)}"}), HTTPStatus.BAD_REQUEST

    podcast_name = data["podcast_name"]
    filename = data["filename"]
    raw_transcription_text = data["raw_transcription_text"]
    title = data.get("title", "")

    try:
        mode = ProcessingMode(data["mode"])
    except ValueError:
        return jsonify({
            "error": f"Invalid mode '{data['mode']}'. Must be one of: {[m.value for m in ProcessingMode]}"
        }), HTTPStatus.BAD_REQUEST

    try:
        transcript = services.process_transcript(
            podcast_name=podcast_name,
            filename=filename,
            raw_transcription_text=raw_transcription_text,
            mode=mode,
            title=title
        )
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    result = asdict(transcript)
    result['mode'] = transcript.mode.value
    return jsonify(result), HTTPStatus.CREATED

@app.route("/transcripts/<int:transcript_id>", methods=["GET"])
def get_transcript(transcript_id: int):
    try:
        transcript = services.get_transcript(transcript_id=transcript_id)
    except ValueError:
        return jsonify({"error": f"transcript with id {transcript_id} not found"}), HTTPStatus.NOT_FOUND

    result = asdict(transcript)
    result['mode'] = transcript.mode.value
    return jsonify(result), HTTPStatus.CREATED


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)