import json
from pathlib import Path
from collections import Counter

GUID = "33ef6bfc-73cc-11f1-aa39-7fd94399ff0a"
SPEAKER_THRESHOLD = 0.03

with open(RAW_DIR / f"{GUID}.json") as f:
    data = json.load(f)

words = json.loads(data["transcription"]["text"])

# Filter logic to highlight primary speakers only (i.e. no ads)
counts = Counter(w["speaker"] for w in words)
total_words = sum(counts.values())
total_speakers = len(counts)
primary_speaker_ids = [
    speaker_id for speaker_id, count in counts.items()
    if count / total_words > SPEAKER_THRESHOLD
]

print(f"Total speaker count: {len(counts)}")
print(f"Primary speaker Ids: {primary_speaker_ids}")
print("Word count per speaker ID (descending):")
for speaker_id, count in counts.most_common():
    print(f"  speaker {speaker_id}: {count} words")