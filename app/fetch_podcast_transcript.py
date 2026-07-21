import os
import json
import requests
from pathlib import Path

TOKEN = os.environ['PODSCRIBE_TOKEN']

GUID = "33ef6bfc-73cc-11f1-aa39-7fd94399ff0a"
ITUNES_ID = "1805478723"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "fetched_raw_transcripts"
RAW_DIR.mkdir(parents=True, exist_ok=True)

response = requests.get(
    "https://backend.podscribe.ai/api/public/episode/transcript",
    headers={"Authorization": f"Bearer {TOKEN}"},
    params={
        "guid": GUID,
        "itunes_or_yt_id": ITUNES_ID,
        "format": "timestamps"
    },
)
response.raise_for_status()
data = response.json()

print("TITLE:", data["title"])
print("\nDESCRIPTION:\n", data["description"])

transcript = json.loads(data["transcription"]["text"])

print("\nTYPE of transcript field:", type(transcript))
print("\nFirst 10 entries of transcript data:")
if isinstance(transcript, list):
    for entry in transcript[:10]:
        print(entry)
else:
    print(transcript[:500])  # fallback if it's actually a string

# Save the FULL raw response so we don't have to re-fetch it later
with open(f"{RAW_DIR}/{GUID}.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"\nSaved full response to {GUID}.json")
