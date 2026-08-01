import abc
from app.models import Transcript


class TranscriptRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def save_transcript(self, transcript: Transcript, podcast_name: str) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get_transcript(self, transcript_id: int) -> Transcript:
        raise NotImplementedError
