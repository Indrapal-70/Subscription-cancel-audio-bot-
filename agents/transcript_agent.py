import os


class TranscriptAgent:
    def __init__(self, filename: str = "transcript.txt"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write("---- Transcript ----\n")

    def save_transcript(self, speaker: str, text: str) -> None:
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"{speaker.upper()}: {text}\n")


