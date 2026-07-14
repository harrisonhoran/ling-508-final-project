import os

import json
from pathlib import Path

# constants for guid, project root, and raw_directory
GUID = "33ef6bfc-73cc-11f1-aa39-7fd94399ff0a"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data / fetched_raw_transcripts"

# Load the already-saved response - no API call needed
with open(RAW_DIR / f"{GUID}.json") as f:
    data = json.load(f)

# The transcript field is a JSON *string* - parse it into a real list
transcript = json.loads(data["transcription"]["text"])

# --- Sanity check: how many distinct speakers actually appear? ---


# --- Group consecutive words by speaker into turns ---

# print total speaker turns on new line


# --- Write clean, speaker-attributed .txt ---
