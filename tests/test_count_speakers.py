import json
from pathlib import Path

import pytest

from app.transcript_processing import (
    calculate_speaker_proportions,
    identify_principal_speakers,
    group_into_turns,
    build_dialogues,
    SPEAKER_THRESHOLD
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIXTURE_PATH = PROJECT_ROOT / "data" / "test_data" / "test_transcript.json"

@pytest.fixture
def real_episode():
    with open(FIXTURE_PATH) as f:
        return json.load(f)

@pytest.fixture
def real_words(real_episode):
    return json.loads(real_episode["transcription"]["text"])


def test_calculate_speaker_proportions_sums_to_one(real_words):
    props =

def test_calculate_speaker_proportions_matches_known_values(real_words):

def test_identify_principal_speakers_keeps_only_those_above_threshold(real_words):

def test_identify_principal_speakers_threshold_is_configurable(real_words):

def test_build_dialogues_excludes_other_speakers_from_main_dialogue(real_words):


def test_count_speakers():
    test_transcript = TEST_TRANSCRIPT
    with open(test_transcript) as f:
        data = json.load(f)

    words = json.loads(data["transcription"]["text"])
    total_speakers = Counter(w["speaker"] for w in words)
    primary_speakers =
    assert speaker_count ==





