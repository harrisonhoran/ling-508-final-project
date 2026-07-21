import pytest
from app.models import *
from app.enums import *


# *************************************************************************
# Test Records/Parameters
# *************************************************************************
DIALOGUE_PARAMS = {
    "speaker":      "Host",
    "text":         "Welcome to the Zach Lowe Show",
    "timestamp":    ""

}

TRANSCRIPT_PARAMS = {
    "podcast_id": test_podcast_params.id,

}

PODCAST_PARAMS = {
    "id": 465283065,
    "name": "the_zach_lowe_show_465283065"
}

# --- Dialogue tests ---
def test_dialogue():
    d = Dialogue(**DIALOGUE_PARAMS)
    assert podcast.id   == 465283065
    assert podcast.name == "the_zach_lowe_show_465283065"
def test_dialogue_creates_with_correct_attributes():


# - d Validation rules -
# Needs to be a string
# Can't have missing fields

# --- Transcript tests ---
def test_transcript():
    podcast = Transcript(**test_transcript_params)
    assert podcast.id   == 465283065
    assert podcast.name == "the_zach_lowe_show_465283065"


# - Transcript Validation Rules -
# Needs to be a string
# Can't have missing fields


# --- Podcast tests ---
def test_podcast():
    podcast = Podcast(**test_podcast_params)
    assert podcast.id   == 465283065
    assert podcast.name == "the_zach_lowe_show_465283065"

