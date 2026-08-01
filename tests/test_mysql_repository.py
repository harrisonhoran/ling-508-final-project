import pytest
from db.mysql_repository import MySQLTranscriptRepository
from app.enums import ProcessingMode
from app.models import Transcript, Dialogue


repo = MySQLTranscriptRepository()

# build a Transcript
def build_transcript(filename_suffix="", with_dialogues=True):
    dialogues = []
    if with_dialogues:
        dialogues = [
            Dialogue(speaker="HOST", text="Welcome to the show", timestamp=2),
            Dialogue(speaker="GUEST", text="Glad to be here", timestamp=4, order=2)
        ]
    return Transcript(
        podcast_id=None,
        filename=f"test_filename_{filename_suffix}.txt",
        raw_text="raw text here",
        clean_text="clean text here",
        mode=ProcessingMode.CLEAN,
        dialogues=dialogues,
    )

# save it, retrieve it, and assert the filename matches
def test_save_and_get_transcript():
    transcript = build_transcript("basic")
    transcript_id = repo.save_transcript(transcript=transcript, podcast_name="Test Podcast A")

    retreived = repo.get_transcript(transcript_id=transcript_id)
    assert retreived.filename == transcript.filename
    assert retreived.raw_text == "raw text here"
    assert retreived.clean_text == "clean text here"
    assert retreived.mode == ProcessingMode.CLEAN