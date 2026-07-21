from app.enums import ProcessingMode
from dataclasses import dataclass, field

@dataclass
class Dialogue:
    speaker: str
    text: str
    timestamp: int
    order: int = 1

# class Dialogue:
#
#     def __init__(self, speaker: str, text: str, timestamp: int, order: int):
#         self.speaker = speaker
#         self.text = text
#         self.timestamp = timestamp
#         self.order = order

@dataclass
class Transcript:
    podcast_id: int
    filename: str
    raw_text: str
    clean_text: str
    mode: ProcessingMode
    dialogues: list[Dialogue] = field(default_factory=list)

# class Transcript:
#
#     def __init__(self, podcast_id: int, filename: str, raw_text: str, clean_text: str, mode = ProcessingMode):
#         self.podcast_id = podcast_id
#         self.filename = filename
#         self.raw_text = raw_text
#         self.clean_text = clean_text
#         self.ProcessingMode = ProcessingMode

@dataclass
class Podcast:
    id: int
    name: str
