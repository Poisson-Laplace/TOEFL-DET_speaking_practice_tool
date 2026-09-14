"""
Selector screen shown when the window launches.
Allows the user to select between TOEFL and DET.
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)


class SelectorScreen(QWidget):
    """
    Landing / Selector Screen to choose between TOEFL and Duolingo English Test.
    """
    exam_selected = pyqtSignal(str)  # "toefl", "det", "free"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #0b0f19;")
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 36, 40, 36)
        main_layout.setSpacing(28)
        main_layout.setAlignment(Qt.AlignCenter)

        # Header Title & Subtitle
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        header_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Speaking Practice Studio")
        title.setStyleSheet("font-size: 34px; font-weight: 800; color: #f8fafc; background: transparent;")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Çalışmak istediğin sınav formatını seçerek başla")
        subtitle.setStyleSheet("font-size: 15px; color: #94a3b8; background: transparent;")
        subtitle.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)

        main_layout.addSpacing(10)

        # Cards Container (Horizontal Layout)
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(24)
        cards_layout.setAlignment(Qt.AlignCenter)

        # ---------------- TOEFL CARD ----------------
        toefl_card = QFrame()
        toefl_card.setStyleSheet("""
            QFrame {
                background-color: #0f1b33;
                border: 2px solid #1e3a8a;
                border-radius: 16px;
                padding: 24px;
                min-width: 360px;
                max-width: 440px;
            }
            QFrame:hover {
                border-color: #3b82f6;
                background-color: #132342;
            }
        """)
        toefl_layout = QVBoxLayout(toefl_card)
        toefl_layout.setSpacing(14)

        toefl_badge = QLabel("TOEFL iBT • 2026 Formatı")
        toefl_badge.setStyleSheet("""
            background-color: #1e3a8a;
            color: #93c5fd;
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 11px;
            font-weight: 700;
        """)

        toefl_title = QLabel("TOEFL Speaking")
        toefl_title.setStyleSheet("font-size: 24px; font-weight: 800; color: #ffffff; background: transparent;")

        toefl_desc = QLabel(
            "<div style='color: #cbd5e1; font-size: 14px; line-height: 1.6;'>"
            "Yeni 2026 sınav formatına uygun spontane konuşma pratiği:<br><br>"
            "<b style='color: #60a5fa;'>[1] 7x Listen & Repeat:</b> Cümleyi duy ve anında tekrar et (0s prep)<br><br>"
            "<b style='color: #60a5fa;'>[2] 4x Take an Interview:</b> 45 saniyelik mülakat cevapları"
            "</div>"
        )
        toefl_desc.setTextFormat(Qt.RichText)
        toefl_desc.setWordWrap(True)
        toefl_desc.setStyleSheet("background: transparent;")

        toefl_btn = QPushButton("TOEFL Modunu Başlat →")
        toefl_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                border: 1px solid #3b82f6;
                color: #ffffff;
                font-size: 15px;
                font-weight: 700;
                padding: 12px 20px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
                border-color: #60a5fa;
            }
        """)
        toefl_btn.setCursor(Qt.PointingHandCursor)
        toefl_btn.clicked.connect(lambda: self.exam_selected.emit("toefl"))

        toefl_layout.addWidget(toefl_badge, alignment=Qt.AlignLeft)
        toefl_layout.addWidget(toefl_title)
        toefl_layout.addWidget(toefl_desc)
        toefl_layout.addSpacing(8)
        toefl_layout.addWidget(toefl_btn)

        cards_layout.addWidget(toefl_card)

        # ---------------- DET CARD ----------------
        det_card = QFrame()
        det_card.setStyleSheet("""
            QFrame {
                background-color: #0c241c;
                border: 2px solid #065f46;
                border-radius: 16px;
                padding: 24px;
                min-width: 360px;
                max-width: 440px;
            }
            QFrame:hover {
                border-color: #10b981;
                background-color: #0f2e24;
            }
        """)
        det_layout = QVBoxLayout(det_card)
        det_layout.setSpacing(14)

        det_badge = QLabel("Duolingo English Test • Güncel Format")
        det_badge.setStyleSheet("""
            background-color: #064e3b;
            color: #6ee7b7;
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 11px;
            font-weight: 700;
        """)

        det_title = QLabel("Duolingo (DET)")
        det_title.setStyleSheet("font-size: 24px; font-weight: 800; color: #ffffff; background: transparent;")

        det_desc = QLabel(
            "<div style='color: #cbd5e1; font-size: 14px; line-height: 1.6;'>"
            "Güncel Duolingo English Test konuşma görevleri:<br><br>"
            "<b style='color: #34d399;'>[1] Speak About the Photo:</b> 20s prep, 90s konuşma<br>"
            "<b style='color: #34d399;'>[2] Read, Then Speak:</b> 20s prep, 90s konuşma<br>"
            "<b style='color: #34d399;'>[3] Interactive Speaking:</b> 6-8 tur, 35s cevap<br>"
            "<b style='color: #34d399;'>[4] Speaking Sample:</b> 30s prep, 3 dk konuşma"
            "</div>"
        )
        det_desc.setTextFormat(Qt.RichText)
        det_desc.setWordWrap(True)
        det_desc.setStyleSheet("background: transparent;")

        det_btn = QPushButton("Duolingo Modunu Başlat →")
        det_btn.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                border: 1px solid #10b981;
                color: #ffffff;
                font-size: 15px;
                font-weight: 700;
                padding: 12px 20px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #047857;
                border-color: #34d399;
            }
        """)
        det_btn.setCursor(Qt.PointingHandCursor)
        det_btn.clicked.connect(lambda: self.exam_selected.emit("det"))

        det_layout.addWidget(det_badge, alignment=Qt.AlignLeft)
        det_layout.addWidget(det_title)
        det_layout.addWidget(det_desc)
        det_layout.addSpacing(8)
        det_layout.addWidget(det_btn)

        cards_layout.addWidget(det_card)

        main_layout.addLayout(cards_layout)

        main_layout.addSpacing(8)

        # Bottom Freestyle Option
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignCenter)

        free_btn = QPushButton("~ Serbest Konuşma Modu (Freestyle Sandbox) ~")
        free_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #94a3b8;
                border: 1px dashed #334155;
                padding: 8px 20px;
                font-size: 13px;
                border-radius: 8px;
            }
            QPushButton:hover {
                color: #f1f5f9;
                border-color: #64748b;
                background-color: #1e293b;
            }
        """)
        free_btn.setCursor(Qt.PointingHandCursor)
        free_btn.clicked.connect(lambda: self.exam_selected.emit("free"))
        bottom_layout.addWidget(free_btn)

        main_layout.addLayout(bottom_layout)
