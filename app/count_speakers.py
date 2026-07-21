import json
from pathlib import Path
from collections import Counter

GUID = "33ef6bfc-73cc-11f1-aa39-7fd94399ff0a"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "fetched_raw_transcripts"

with open(RAW_DIR / f"{GUID}.json") as f:
    data = json.load(f)

words = json.loads(data["transcription"]["text"])

counts = Counter(w["speaker"] for w in words)

print("Word count per speaker ID (descending):")
for speaker_id, count in counts.most_common():
    print(f"  speaker {speaker_id}: {count} words")