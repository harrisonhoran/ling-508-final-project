"""
Domain logic for cleaning a raw podcast transcript.

This module is deliberately I/O-free: it takes data in, returns data out,
so it can be unit-tested without touching the filesystem, a network, or a
database. The service layer (app/services.py) is what wires this logic up
to the repository.
"""

import json
from pathlib import Path
from collections import Counter

from app.models import Dialogue

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "fetched_raw_transcripts"
DEFAULT_SPEAKER_THRESHOLD = 0.03

def parse_words(raw_transcription_text: str) -> list[dict]:
    """
    The Podscribe API returns transcription text as a JSON-encoded string
    of word-level entries.
    """
    return json.loads(raw_transcription_text)

def calculate_speaker_proportions(words: list[dict]) -> dict[int, float]:
    """
    Returns each raw speaker id's share of total words, e.g. {0: 0.5555, 3: 0.4042, ...}.
    Values sum to 1.0 across all speakers.
    """
    word_counts = Counter(w["speaker"] for w in words)
    total_words = sum(word_counts.values())
    return {
        speaker_id: count / total_words
        for speaker_id, count in word_counts.items()
    }

def label_principal_speakers(
        words: list[dict], threshold: float = DEFAULT_SPEAKER_THRESHOLD
) -> dict[int, str]:
    """
    Filtering primary speakers (host(s) and guest(s)) from other speakers
    (ad reads, interstitial voices, etc.). So: keep any speaker id whose
    proportion of total words is above `threshold`, label everyone else "OTHER".

    Real speakers are labeled SPEAKER_1, SPEAKER_2, ... in order of first
    chronological appearance in the transcript.
    """
    speaker_props = calculate_speaker_proportions(words=words)
    primary_speaker_ids = {
        speaker_id for speaker_id, prop in speaker_props.items()
        if prop > threshold
    }

    first_appearance_order = []
    for w in words:
        if w["speaker"] in primary_speaker_ids and w["speaker"] not in first_appearance_order:
            first_appearance_order.append(w["speaker"])

    speaker_map = {}
    for i, speaker_id in enumerate(first_appearance_order, start=1):
        speaker_map[speaker_id] = f"SPEAKER_{i}"

    for speaker_id in speaker_props:
        if speaker_id not in speaker_map:
            speaker_map[speaker_id] = "OTHER"

    return speaker_map

def group_into_turns(words: list[dict]) -> list[dict]:
    """
    Collapse consecutive words from the same speaker into a single "turn":
        {"speaker": 0, "text": "This episode is...", "start_time": 0.115}
    """
    turns = []
    current_speaker = None
    current_words = []
    current_start = None

    for w in words:
        if w["speaker"] != current_speaker:
            if current_words:
                turns.append({
                    "speaker": current_speaker,
                    "text": " ".join(current_words),
                    "start": current_start,
                })
            current_speaker = w["speaker"]
            current_words = [w["word"]]
            current_start = w.get("startTime", 0)
        else:
            current_words.append(w["word"])
    if current_words:
        turns.append({
            "speaker": current_speaker,
            "text": " ".join(current_words),
            "start": current_start,
        })

    return turns


def build_dialogues(
    turns: list[dict], speaker_map: dict[int, str]
) -> tuple[list[Dialogue], list[dict]]:
    """
    Converts raw turns into labeled Dialogue objects, using speaker_map
    (from identify_principal_speakers) to decide the label.

    Returns a tuple:
      - dialogues: turns from real speakers (SPEAKER_1, SPEAKER_2, ...),
        in order, ready for the main cleaned transcript.
      - excluded_turns: turns from "OTHER" (ad/noise) speakers, kept
        separately for inspection rather than silently discarded.
    """
    dialogues = []
    excluded_turns = []
    order = 1

    for t in turns:
        label = speaker_map.get(t["speaker"], "OTHER")
        if label == "OTHER":
            excluded_turns.append({
                "speaker_id": t["speaker_id"],
                "text": t["text"],
                "start_time": t["start_time"],
            })
            continue
        dialogues.append(Dialogue(
            speaker=label,
            text=t["text"],
            timestamp=int(t["start_time"] or 0),
            order=order,
        ))
        order += 1

    return dialogues, excluded_turns

def build_clean_text(dialogues: list[Dialogue], title: str = "") -> str:
    lines = []
    if title:
        lines.append(title)
        lines.append("")

    for d in dialogues:
        lines.append(f"{d.speaker}: {d.text}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"

if __name__ == "__main__":
    pass