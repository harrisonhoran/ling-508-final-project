import json
import pytest

from app.enums import ProcessingMode
from app.models import Transcript
from app.services import TranscriptService
from db.repository import TranscriptRepository


class FakeTranscriptRepository(TranscriptRepository):
    """
    Stand-in for MySQLTranscriptRepository. Allows for testing of the
    service layer's logic in isolation, with no real database involved.
    """
    def __init__(self):
        self._store: dict[int, Transcript] = {}
        self._next_id = 1

    def save_transcript(self, transcript: Transcript, podcast_name: str) -> int:
        transcript_id = self._next_id
        self._next_id += 1
        transcript.podcast_id = transcript_id
        self._store[transcript_id] = transcript
        return transcript_id

    def get_transcript(self, transcript_id: int) -> Transcript:
        if transcript_id not in self._store:
            raise ValueError(f"No transcript with id {transcript_id} was found")
        return self._store[transcript_id]


# --- sample raw transcription payload, same shape the Podscribe API returns ---
RAW_WORDS = [
    {"startTime": 0.1, "endTime": 0.4, "speaker": 0, "word": "Welcome"},
    {"startTime": 0.4, "endTime": 0.7, "speaker": 0, "word": "back."},
    {"startTime": 1.0, "endTime": 1.3, "speaker": 1, "word": "Thanks"},
    {"startTime": 1.3, "endTime": 1.6, "speaker": 1, "word": "for"},
    {"startTime": 1.6, "endTime": 1.9, "speaker": 1, "word": "having"},
    {"startTime": 1.9, "endTime": 2.1, "speaker": 1, "word": "me."},
]
RAW_TRANSCRIPTION_TEXT = json.dumps(RAW_WORDS)


@pytest.fixture
def service():
    return TranscriptService(repository=FakeTranscriptRepository())


def test_store_only_mode_keeps_raw_text_and_skips_cleaning(service):
    result = service.process_transcript(
        podcast_name="Test Podcast",
        filename="episode1.txt",
        raw_transcription_text=RAW_TRANSCRIPTION_TEXT,
        mode=ProcessingMode.STORE_ONLY,
    )

    assert result.mode == ProcessingMode.STORE_ONLY
    assert result.raw_text == RAW_TRANSCRIPTION_TEXT
    assert result.clean_text == ""
    assert result.dialogues == []


def test_clean_mode_groups_words_into_labeled_dialogue_turns(service):
    result = service.process_transcript(
        podcast_name="Test Podcast",
        filename="episode1.txt",
        raw_transcription_text=RAW_TRANSCRIPTION_TEXT,
        mode=ProcessingMode.CLEAN,
        title="Test Episode",
    )

    assert result.mode == ProcessingMode.CLEAN
    assert len(result.dialogues) == 2

    # With only 2 real speakers in this sample and expected_count=2 (1 host +
    # 1 guest from the description), both turns are "real" -- neither gets
    # excluded as OTHER/ad noise.
    assert result.dialogues[0].speaker == "SPEAKER_1"
    assert result.dialogues[0].text == "Welcome back."
    assert result.dialogues[0].order == 1

    assert result.dialogues[1].speaker == "SPEAKER_2"
    assert result.dialogues[1].text == "Thanks for having me."
    assert result.dialogues[1].order == 2

    assert "SPEAKER_1: Welcome back." in result.clean_text
    assert "SPEAKER_2: Thanks for having me." in result.clean_text


def test_process_transcript_persists_via_repository_not_in_memory_only(service):
    result = service.process_transcript(
        podcast_name="Test Podcast",
        filename="episode1.txt",
        raw_transcription_text=RAW_TRANSCRIPTION_TEXT,
        mode=ProcessingMode.CLEAN,
    )

    # A podcast_id was assigned by the repository, proving save+retrieve
    # round-tripped through the repository interface rather than the
    # service just returning what it was handed.
    assert result.podcast_id is not None

    fetched_again = service.repository.get_transcript(result.podcast_id)
    assert fetched_again.filename == "episode1.txt"


def test_unsupported_mode_raises(service):
    with pytest.raises(ValueError):
        service.process_transcript(
            podcast_name="Test Podcast",
            filename="episode1.txt",
            raw_transcription_text=RAW_TRANSCRIPTION_TEXT,
            mode="not_a_real_mode",
        )
