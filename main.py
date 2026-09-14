"""
Speaking Practice Studio - TOEFL iBT & Duolingo English Test (DET)
Main Desktop Application Window
"""

import sys
import os

# Add directory to python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QPalette, QColor

from ui.theme import DARK_THEME_QSS
from ui.selector_screen import SelectorScreen
from ui.studio_screen import StudioScreen


class MainWindow(QMainWindow):
    """
    Main Application Window holding the Selector and Studio screens.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Speaking Practice Studio — TOEFL & Duolingo English Test")
        self.resize(1140, 820)
        self.setMinimumSize(980, 700)

        # Force pure dark background on QMainWindow
        self.setStyleSheet("background-color: #f4f7fb;")

        # Central Stacked Widget
        self.stack = QStackedWidget(self)
        self.stack.setStyleSheet("background-color: #f4f7fb;")
        self.setCentralWidget(self.stack)

        # Screen 1: Selector Screen (TOEFL vs DET)
        self.selector_screen = SelectorScreen(self)
        self.selector_screen.exam_selected.connect(self._on_exam_selected)
        self.selector_screen.language_changed.connect(self._on_language_changed)
        self.stack.addWidget(self.selector_screen)

        # Screen 2: Studio Screen (Recording & Word-Level STT)
        self.studio_screen = StudioScreen(self)
        self.studio_screen.back_to_selector.connect(self._on_back_to_selector)
        self.studio_screen.language_changed.connect(self._on_language_changed)
        self.stack.addWidget(self.studio_screen)

        # Start on Selector Screen
        self.stack.setCurrentIndex(0)

    def _on_exam_selected(self, exam_key: str):
        self.studio_screen.set_exam(exam_key)
        self.stack.setCurrentIndex(1)

    def _on_back_to_selector(self):
        self.stack.setCurrentIndex(0)

    def _on_language_changed(self, language: str):
        """Keep both language switches synchronized without signal loops."""
        self.selector_screen.set_language_silent(language)
        self.studio_screen.set_language(language, emit=False)

    def closeEvent(self, event):
        # Stop any ongoing recording or audio playback gracefully
        if hasattr(self.studio_screen, "recorder") and self.studio_screen.recorder.is_recording:
            self.studio_screen.recorder.stop_recording()
        if hasattr(self.studio_screen, "player"):
            self.studio_screen.player.stop()
        event.accept()


def main():
    # Enable High-DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME_QSS)

    # Set dark palette for native dialogs
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#f4f7fb"))
    palette.setColor(QPalette.WindowText, QColor("#172033"))
    palette.setColor(QPalette.Base, QColor("#ffffff"))
    palette.setColor(QPalette.AlternateBase, QColor("#f8fafc"))
    palette.setColor(QPalette.ToolTipBase, QColor("#172033"))
    palette.setColor(QPalette.ToolTipText, QColor("#ffffff"))
    palette.setColor(QPalette.Text, QColor("#172033"))
    palette.setColor(QPalette.Button, QColor("#ffffff"))
    palette.setColor(QPalette.ButtonText, QColor("#24324a"))
    palette.setColor(QPalette.BrightText, QColor("#ef4444"))
    palette.setColor(QPalette.Highlight, QColor("#2457a6"))
    palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
