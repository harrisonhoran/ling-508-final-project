from db.repository import *
from app.models import Dialogue
from app.enums import ProcessingMode
import mysql.connector

class MySQLTranscriptRepository(TranscriptRepository):

    def __init__(self):
        super().__init__()
        config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',  # When you run this on your machine change it to 'localhost'
            # 'host': 'localhost',
            'port': '3306',  # When you run this on your machine change it to '32000'
            # 'port': '32000',
            'database': 'transcript_parser_app'
        }
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    # --- private helper methods ------------------------------------------------------
    def _get_or_create_podcast_id(self, podcast_name: str) -> int:
        self.cursor.execute(
            "SELECT id FROM podcast WHERE name = %s", (podcast_name,)
        )
        row = self.cursor.fetchone()
        if row:
            return row[0]

        self.cursor.execute(
            "INSERT INTO podcast (name) VALUES (%s)", (podcast_name,)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def _insert_dialogue(self, transcript_id: int, dialogue: Dialogue) -> None:
        sql = """
            INSERT INTO dialogue (transcript_id, speaker, text, timestamp, `order`)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(
            sql,
            (transcript_id, dialogue.speaker, dialogue.text, dialogue.timestamp, dialogue.order)
        )

    def _row_to_transcript(self, row, dialogues: list[Dialogue]) -> Transcript:
        (id_, podcast_id, filename, raw_text, clean_text, mode) = row
        return Transcript(
            podcast_id=podcast_id,
            filename=filename,
            raw_text=raw_text,
            clean_text=clean_text,
            mode=ProcessingMode(mode),
            dialogues=dialogues,
        )


    # --- standard methods -----------------------------------------------------------
    def save_transcript(self, transcript: Transcript, podcast_name: str) -> int:
        podcast_id = self._get_or_create_podcast_id(podcast_name=podcast_name)
        sql = """
            INSERT INTO transcript (podcast_id, filename, raw_text, clean_text, mode) 
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(
            sql,
            (podcast_id, transcript.filename, transcript.raw_text,
             transcript.clean_text, transcript.mode.value)
        )
        transcript_id = self.cursor.lastrowid

        for dialogue in transcript.dialogues:
            self._insert_dialogue(transcript_id, dialogue)

        self.connection.commit()
        return transcript_id

    def get_transcript(self, transcript_id: int) -> Transcript:
        self.cursor.execute(
        "SELECT id, podcast_id, filename, raw_text, clean_text, mode " 
        "FROM transcript WHERE id = %s",
        (transcript_id,)
        )
        row = self.cursor.fetchone()
        if row is None:
            raise ValueError(f"No transcript with id {transcript_id} was found")

        self.cursor.execute(
            "SELECT speaker, text, timestamp, `order` "
            "FROM dialogue WHERE transcript_id = %s ORDER BY `order`",
            (transcript_id,)
        )
        dialogues = [
            Dialogue(speaker=speaker, text=text, timestamp=timestamp, order=order)
            for (speaker, text, timestamp, order) in self.cursor
        ]

        return self._row_to_transcript(row, dialogues)