from app.enums import ProcessingMode
from dataclasses import dataclass, field

@dataclass
class Dialogue:
    speaker: str
    text: str
    timestamp: int
    order: int = 1

@dataclass
class Transcript:
    podcast_id: int
    filename: str
    raw_text: str
    clean_text: str
    mode: ProcessingMode
    dialogues: list[Dialogue] = field(default_factory=list)
    excluded_speaker_turns: list[dict] = field(default_factory=list)

@dataclass
class Podcast:
    name: str
    id: int = None
