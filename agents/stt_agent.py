import json
import os


class STTAgent:
    def __init__(self, model_path: str | None = None, language_code: str = "he"):
        self._vosk = None
        self._vosk_model = None
        self._language_code = language_code
        self._explicit_model_path = model_path

        try:
            import vosk  # type: ignore

            self._vosk = vosk
        except Exception:
            self._vosk = None

    def _ensure_model(self) -> None:
        if self._vosk is None:
            raise RuntimeError(
                "Vosk is not installed. Install 'vosk' and a Hebrew model to enable STT."
            )

        if self._vosk_model is not None:
            return

        model_path = self._explicit_model_path or os.getenv("VOSK_MODEL_PATH")
        try:
            if model_path and os.path.exists(model_path):
                self._vosk_model = self._vosk.Model(model_path)
            else:
                self._vosk_model = self._vosk.Model(lang=self._language_code)
        except Exception as exc:
            raise RuntimeError(
                "Vosk Hebrew model not found. Set VOSK_MODEL_PATH to the extracted model directory "
                "or pass model_path to STTAgent(...)."
            ) from exc

    def speech_to_text(self, audio_file: str) -> str:
        self._ensure_model()

        import soundfile as sf  # type: ignore

        with sf.SoundFile(audio_file) as f:
            audio = f.read(dtype="int16")
            rec = self._vosk.KaldiRecognizer(self._vosk_model, f.samplerate)
            rec.AcceptWaveform(audio.tobytes())
            result = json.loads(rec.FinalResult())
            return result.get("text", "")


