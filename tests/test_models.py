import pytest
from app.models import *
from app.enums import *

# *************************************************************************
# Test Records/Parameters
# *************************************************************************
DIALOGUE_PARAMS = {
    "speaker": "host",
    "text": "welcome to the zach lowe show",
    "timestamp": 1783683061,
    "order": 1,
}

TRANSCRIPT_PARAMS = {
    "podcast_id": 465283065,
    "filename": "the_zach_lowe_show_465283065.txt",
    "raw_text": "brought to you by",
    "clean_text": "state farm",
    "mode": ProcessingMode.CLEAN,
}

# --- Dialogue tests ---
def test_dialogue():
    d = Dialogue(**DIALOGUE_PARAMS)
    assert d.speaker == "host"
    assert d.text == "welcome to the zach lowe show"
    assert d.timestamp == 1783683061
    assert d.order == 1


# --- Transcript tests ---
def test_transcript():
    t = Transcript(**TRANSCRIPT_PARAMS)
    assert t.podcast_id == 465283065
    assert t.filename == "the_zach_lowe_show_465283065.txt"
    assert t.raw_text == "brought to you by"
    assert t.clean_text == "state farm"
    assert t.mode == ProcessingMode.CLEAN
