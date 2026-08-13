from http import HTTPStatus

import pytest
from main import app

@pytest.fixture
def client():
    return app.test_client()

def test_end_to_end_create_get_transcript(client):
    payload = {
        "podcast_name": "E2E Pod Test",
        "filename": "e2e_test.txt",
        "raw_transcription_text": '[{"speaker":0,"word":"Hi","startTime":0},{"speaker":0,"word":"there","startTime":0.5}]',
        "mode": "clean",
    }

    create_response = client.post("/transcripts", json=payload)
    assert create_response.status_code == 201
    created = create_response.get_json()
    assert created["dialogues"][0]["text"] == "Hi there"

    transcript_id = created["id"]

    get_response = client.get(f"/transcripts/{transcript_id}")
    assert get_response.status_code == 200
    assert get_response.get_json()["filename"] == "e2e_test.txt"