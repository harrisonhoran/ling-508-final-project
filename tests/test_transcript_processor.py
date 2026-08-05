import json
from pathlib import Path

import pytest

from app import transcript_processor
from app.transcript_processor import (
    calculate_speaker_proportions,
    label_primary_speakers,
    group_into_turns,
    build_dialogues,
)

FIXTURE_PATH = Path(__file__).resolve().parent.parent / "data" / "test_data" / "test_transcript.json"

@pytest.fixture
def real_episode():
    with open(FIXTURE_PATH) as f:
        return json.load(f)

@pytest.fixture
def real_words(real_episode):
    return json.loads(real_episode["transcription"]["text"])

def test_calculate_speaker_proportions(real_words):
    speaker_props = calculate_speaker_proportions(real_words)
    assert len(speaker_props) == 9
    assert sum(speaker_props.values()) == pytest.approx(1.0)

