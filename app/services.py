"""
Service layer: coordinates the business logic of the app. Dependent
on the abstract TranscriptRepository interface, but not on MySQL directly,
so it can be tested with a fake repo.
"""
from app.enums import ProcessingMode
from app.models import Transcript
from app.transcript_processor import (
    parse_words,
    group_into_turns,
    build_dialogues,
    build_clean_text,
    label_primary_speakers,
    DEFAULT_SPEAKER_THRESHOLD
)
from db.repository import TranscriptRepository


class TranscriptService:
    def __init__(self, repository: TranscriptRepository):
        self.repository = repository

    def process_transcript(
            self,
            podcast_name: str,
            filename: str,
            raw_transcription_text: str,
            mode: ProcessingMode,
            title: str = "",
            speaker_threshold: float = DEFAULT_SPEAKER_THRESHOLD,
    ) -> Transcript:
        """
        Implements ProcessingMode functionality from week 1 use cases:
        STORE_ONLY: just save raw transcript, as is
        CLEAN: run transcript processor to clean and return text
        """
        if mode == ProcessingMode.STORE_ONLY:
            transcript = Transcript(
                podcast_id=None,
                filename=filename,
                raw_text=raw_transcription_text,
                clean_text="",
                mode=mode,
                dialogues=[],
            )
        elif mode == ProcessingMode.CLEAN:
            words = parse_words(raw_transcription_text)
            turns = group_into_turns(words)

            speaker_map = label_primary_speakers(words, threshold=speaker_threshold)

            dialogues, excluded_turns = build_dialogues(turns, speaker_map)
            clean_text = build_clean_text(dialogues, title=title)
            transcript = Transcript(
                podcast_id=None,
                filename=filename,
                raw_text=raw_transcription_text,
                clean_text=clean_text,
                mode=mode,
                dialogues=dialogues,
            )
        else:
            raise ValueError(f"Unsupported processing mode: {mode}")

        transcript_id = self.repository.save_transcript(transcript, podcast_name)
        saved_transcript = self.repository.get_transcript(transcript_id)
        if mode == ProcessingMode.CLEAN:
            saved_transcript.excluded_speaker_turns = excluded_turns
        return saved_transcript