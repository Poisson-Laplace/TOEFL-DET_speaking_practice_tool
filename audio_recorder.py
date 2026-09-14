"""
Audio recording module using ffmpeg pulse/alsa input for high quality 16kHz WAV recordings.
"""

import os
import time
import subprocess
from datetime import datetime
from PyQt5.QtCore import QObject, QTimer, pyqtSignal

RECORDINGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recordings")
os.makedirs(RECORDINGS_DIR, exist_ok=True)


class AudioRecorder(QObject):
    """
    Manages microphone recording using an ffmpeg subprocess.
    Emits duration updates and final output filepath.
    """
    started = pyqtSignal(str)              # output_path
    tick = pyqtSignal(int)                 # elapsed seconds
    finished = pyqtSignal(str, int)        # output_path, total_seconds
    error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.process = None
        self.output_path = None
        self.start_time = None
        self.elapsed_seconds = 0
        self.max_duration = None

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._on_tick)

    @property
    def is_recording(self) -> bool:
        return self.process is not None and self.process.poll() is None

    def start_recording(self, prefix: str = "session", max_duration: int = None) -> str:
        if self.is_recording:
            return self.output_path
        
        self.max_duration = max_duration

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.wav"
        self.output_path = os.path.join(RECORDINGS_DIR, filename)

        # Prefer pulse input on modern Linux, with fallback to default
        cmd = [
            "ffmpeg",
            "-y",
            "-f", "pulse",
            "-i", "default",
            "-ac", "1",
            "-ar", "16000",
            self.output_path
        ]

        try:
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.start_time = time.time()
            self.elapsed_seconds = 0
            self.timer.start()
            self.started.emit(self.output_path)
            return self.output_path
        except Exception as exc:
            self.error.emit(f"Ses kaydı başlatılamadı: {exc}")
            return ""

    def _on_tick(self):
        if self.start_time:
            self.elapsed_seconds = int(time.time() - self.start_time)
            self.tick.emit(self.elapsed_seconds)
            
            # Automatically stop if max duration is reached
            if self.max_duration is not None and self.elapsed_seconds >= self.max_duration:
                self.stop_recording()

    def stop_recording(self) -> str:
        if not self.is_recording:
            return self.output_path or ""

        self.timer.stop()
        final_path = self.output_path
        final_duration = self.elapsed_seconds

        try:
            # Send 'q' to ffmpeg to flush headers cleanly
            if self.process.stdin:
                try:
                    self.process.stdin.write(b"q")
                    self.process.stdin.flush()
                except Exception:
                    pass

            try:
                self.process.wait(timeout=2.0)
            except subprocess.TimeoutExpired:
                self.process.terminate()
                self.process.wait(timeout=1.0)
        except Exception as exc:
            self.error.emit(f"Kayıt durdurulurken hata: {exc}")
        finally:
            self.process = None

        if os.path.exists(final_path) and os.path.getsize(final_path) > 100:
            self.finished.emit(final_path, final_duration)
            return final_path
        else:
            self.error.emit("Kayıt dosyası oluşturulamadı veya boş.")
            return ""
