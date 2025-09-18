import os


class TTSAgent:
    def __init__(self, output_dir="voices"):
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir

        self._coqui_tts = None
        try:
            from TTS.api import TTS  # type: ignore
            self._coqui_tts = TTS(
                model_name="tts_models/multilingual/multi-dataset/your_tts",
                progress_bar=False,
                gpu=False,
            )
        except Exception:
            self._coqui_tts = None

        self._gtts = None
        if self._coqui_tts is None:
            try:
                from gtts import gTTS  # type: ignore

                self._gtts = gTTS
            except Exception:
                self._gtts = None

    def text_to_speech(self, text: str, filename: str = "output.wav") -> str:
        path = os.path.join(self.output_dir, filename)

        if self._coqui_tts is not None:
            self._coqui_tts.tts_to_file(text=text, file_path=path)
            return path

        if self._gtts is not None:
            if not path.lower().endswith(".mp3"):
                path = os.path.splitext(path)[0] + ".mp3"
            try:
                tts = self._gtts(text=text, lang="he")
            except Exception:
                tts = self._gtts(text=text, lang="iw")
            tts.save(path)
            return path

        raise RuntimeError(
            "No TTS backend available. Install Coqui TTS (preferred) or gTTS."
        )


