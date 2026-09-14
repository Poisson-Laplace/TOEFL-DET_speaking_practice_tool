"""
Speech-to-Text engine using faster-whisper with word-level timestamps.
Runs in a background QThread to keep the PyQt5 GUI 100% responsive.
"""

import os
import time
from PyQt5.QtCore import QThread, pyqtSignal
from faster_whisper import WhisperModel

_MODEL_CACHE = None


def get_whisper_model(model_name: str = "base.en"):
    """
    Singleton loader for faster-whisper model.
    Loads onto CPU with int8 precision (optimized for high speed and low memory).
    """
    global _MODEL_CACHE
    if _MODEL_CACHE is None:
        _MODEL_CACHE = WhisperModel(model_name, device="cpu", compute_type="int8")
    return _MODEL_CACHE


class TranscribeWorker(QThread):
    """
    Background worker thread for audio transcription with word-level timestamps.
    """
    started_signal = pyqtSignal()
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)

    def __init__(self, audio_path: str, model_name: str = "base.en", parent=None):
        super().__init__(parent)
        self.audio_path = audio_path
        self.model_name = model_name

    def run(self):
        try:
            self.started_signal.emit()
            self.progress_signal.emit("STT Modeli hazırlanıyor...")

            if not os.path.exists(self.audio_path):
                self.error_signal.emit(f"Ses dosyası bulunamadı: {self.audio_path}")
                return

            t_start = time.time()
            model = get_whisper_model(self.model_name)

            self.progress_signal.emit("Kelimeler ve zaman damgaları çıkarılıyor...")
            segments, info = model.transcribe(
                self.audio_path,
                word_timestamps=True,
                language="en",
                beam_size=5,
                vad_filter=True,
            )

            words_data = []
            full_text_parts = []
            word_idx = 1

            for segment in segments:
                full_text_parts.append(segment.text.strip())
                if segment.words:
                    for w in segment.words:
                        cleaned_word = w.word.strip()
                        if cleaned_word:
                            w_start = float(max(0.0, round(float(w.start), 2)))
                            w_end = float(max(w_start, round(float(w.end), 2)))
                            words_data.append({
                                "id": word_idx,
                                "word": cleaned_word,
                                "start": w_start,
                                "end": w_end,
                                "duration": float(round(w_end - w_start, 2)),
                                "probability": float(round(float(w.probability), 2)),
                            })
                            word_idx += 1

            full_text = " ".join(full_text_parts).strip()
            total_duration = float(round(float(info.duration), 2)) if info and info.duration else 0.0

            # Calculate WPM (Words Per Minute)
            if total_duration > 0 and words_data:
                wpm = float(round(float(len(words_data)) / (total_duration / 60.0), 1))
            else:
                wpm = 0.0

            elapsed = float(round(float(time.time() - t_start), 2))
            result = {
                "audio_path": self.audio_path,
                "full_text": full_text,
                "duration": total_duration,
                "words": words_data,
                "word_count": len(words_data),
                "wpm": wpm,
                "process_time": elapsed,
            }

            self.finished_signal.emit(result)

        except Exception as exc:
            self.error_signal.emit(str(exc))
