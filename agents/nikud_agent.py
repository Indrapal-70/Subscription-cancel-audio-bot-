from typing import Optional
import os


class NikudAgent:
    def __init__(self, model_path: str = "./phonikud-1.0.int8.onnx"):
        self.model_path = model_path
        self._model: Optional[object] = None

        try:
            from phonikud_onnx import Phonikud  # type: ignore

            if not os.path.exists(self.model_path):
                raise FileNotFoundError(
                    f"Phonikud ONNX model not found at {self.model_path}. Place the model file there or pass model_path."
                )
            self._model = Phonikud(self.model_path)
        except Exception as exc:
            # Defer failure to call time if model is not available
            self._model = None
            self._init_error = exc
        try:
            from phonikud import phonemize  # type: ignore

            self._phonemize = phonemize
        except Exception:
            self._phonemize = None

    def add_nikud(self, hebrew_text: str) -> str:
        if self._model is None:
            raise RuntimeError(
                f"Phonikud ONNX model not loaded from {self.model_path}: {self._init_error}"
                if hasattr(self, "_init_error")
                else f"Phonikud ONNX model not loaded from {self.model_path}"
            )

        vocalized = self._model.add_diacritics(hebrew_text)
        return vocalized

    def add_nikud_and_phonemes(self, hebrew_text: str) -> tuple[str, Optional[str]]:
        vocalized = self.add_nikud(hebrew_text)
        if getattr(self, "_phonemize", None):
            try:
                phonemes = self._phonemize(vocalized)  # type: ignore[attr-defined]
            except Exception:
                phonemes = None
        else:
            phonemes = None
        return vocalized, phonemes
