import json
from pathlib import Path
from collections import Counter

from app.count_speakers import speaker_id

# constants for guid, project root, and raw_directory
GUID = "33ef6bfc-73cc-11f1-aa39-7fd94399ff0a"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "fetched_raw_transcripts"
CLEAN_DIR = PROJECT_ROOT / "data" / "clean_transcripts"

# Load JSON
with open(RAW_DIR / f"{GUID}.json") as f:
    data = json.load(f)

# Parse JSON into string
words = json.loads(data["transcription"]["text"])

count_words = Counter(w["speaker"] for w in words)
ranked_speakers = [speaker_id for speaker_id, _ in count_words.most_common()]

# --- Sanity check: how many distinct speakers actually appear? ---
speaker_ids = sorted(set(w["speaker"] for w in words))
print(f"Distinct speakers found: {speaker_ids}")
print("Total transcript word count: ", len(words))

max_speaker = max(speaker_ids)

def label_speaker(speaker_id):
    return "GUEST" if speaker_id == max_speaker else "HOST"

# --- Group consecutive words by speaker into turns ---
turns = []
current_speaker = "none"
current_words = []

for w in words:
    if w["speaker"] != current_speaker:
        if current_words:
            turns.append((current_speaker, " ".join(current_words)))
        current_speaker = w["speaker"]
        current_words = [w["word"]]
    else:
        current_words.append(w["word"])

if current_words:
    turns.append((current_speaker, " ".join(current_words)))

# print total speaker turns on new line
print(f"\nTotal speaker turns: {len(turns)}")

# --- Write clean, speaker-attributed .txt ---
seriesTitleClean = data["seriesTitle"].replace(" ", "_").lower()
guid_suffix_six  = data["guid"][-6]
filename_base    = f"{seriesTitleClean}_{guid_suffix_six}"

out_path = CLEAN_DIR / f"{seriesTitleClean}_clean.txt"
with open(out_path, "w") as f:
    f.write(f"{seriesTitleClean}\n\n")
    for speaker_id, text in turns:
        f.write(f"{label_speaker(speaker_id)}: {text}\n\n")

print(f"Saved {out_path}")