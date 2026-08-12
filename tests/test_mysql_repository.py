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

def test_podcast_is_reused_not_duplicated():
    t1 = build_transcript("dedup1")
    t2 = build_transcript("dedup2")

    id1 = repo.save_transcript(t1, podcast_name="Same Podcast")
    id2 = repo.save_transcript(t2, podcast_name="Same Podcast")

    ret1 = repo.get_transcript(id1)
    ret2 = repo.get_transcript(id2)

    assert ret1.podcast_id == ret2.podcast_id

def test_dialogues_round_trip_in_order():
    transcript = build_transcript("dialogues")
    transcript_id = repo.save_transcript(transcript, podcast_name="Test Podcast B")

    ret = repo.get_transcript(transcript_id)

    assert len(ret.dialogues) == 2
    assert ret.dialogues[0].speaker == "HOST"
    assert ret.dialogues[0].order == 1
    assert ret.dialogues[1].speaker == "GUEST"
    assert ret.dialogues[1].order == 2

def test_get_transcript_missing_id_raises():
    with pytest.raises(ValueError):
        repo.get_transcript(999999999)


@pytest.fixture(autouse=True)
def cleanup_test_data():
    yield  # test runs here
    # after the test finishes (pass or fail), clean up everything it created
    repo.cursor.execute("DELETE FROM dialogue")
    repo.cursor.execute("DELETE FROM transcript")
    repo.cursor.execute("DELETE FROM podcast")
    repo.connection.commit()