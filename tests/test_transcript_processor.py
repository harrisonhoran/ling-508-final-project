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

