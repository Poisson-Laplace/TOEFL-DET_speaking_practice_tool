from PyQt5.QtCore import QThread, pyqtSignal
from gtts import gTTS
import os
import tempfile

class TTSWorker(QThread):
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text

    def run(self):
        try:
            tts = gTTS(text=self.text, lang='en', slow=False)
            fd, path = tempfile.mkstemp(suffix=".mp3")
            os.close(fd)
            tts.save(path)
            self.finished_signal.emit(path)
        except Exception as e:
            self.error_signal.emit(str(e))
