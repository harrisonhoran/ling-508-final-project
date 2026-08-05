import json
from pathlib import Path

import pytest

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

def test_label_primary_speakers_keeps_only_those_above_threshold(real_words):
    speaker_map = label_primary_speakers(real_words, 0.03)

    primary_labels = [label for label in speaker_map.values() if label != "OTHER"]
    assert len(primary_labels) == 2
    assert set(primary_labels) == {"SPEAKER_1", "SPEAKER_2"}
    assert speaker_map[9] == "OTHER"

def test_label_primary_speakers_threshold_is_configurable(real_words):
    speaker_map = label_primary_speakers(real_words, 0.8)
    assert all(label == "OTHER" for label in speaker_map.values())

def test_build_dialogues_excludes_other_speakers_from_main_dialogue(real_words):
    turns = group_into_turns(real_words)
    speaker_map = label_primary_speakers(real_words, threshold=0.03)
    dialogues, excluded_turns = build_dialogues(turns, speaker_map)

    # Testing false positive
    assert all(d.speaker != "OTHER" for d in dialogues)

    # Testing true negative
    assert len(excluded_turns) > 0
    assert all("speaker_id" in t for t in excluded_turns)
