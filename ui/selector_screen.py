"""Welcoming exam selector with synchronized Turkish/English controls."""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame

from ui.language_switch import LanguageSwitch


TEXT = {
    "tr": {
        "eyebrow": "KONUŞMA PRATİĞİ",
        "title": "Bugün hangi sınava hazırlanıyorsun?",
        "subtitle": "Sınav formatını seç. Sonraki ekranda görev türünü değiştirebilirsin.",
        "toefl_badge": "GÜNCEL 2026 FORMATI",
        "toefl_desc": "Akademik yaşam odaklı yeni speaking deneyimi.",
        "toefl_one": "7 × Dinle ve Tekrar Et",
        "toefl_two": "4 × Mülakat Sorusu",
        "toefl_btn": "TOEFL çalışmasına başla",
        "det_badge": "GÜNCEL DET FORMATI",
        "det_desc": "Kısa, görsel ve etkileşimli konuşma görevleri.",
        "det_one": "Fotoğraf • Okuma • Etkileşim",
        "det_two": "Speaking Sample",
        "det_btn": "DET çalışmasına başla",
        "free": "Serbest konuşma alanını aç",
        "language": "Arayüz dili",
    },
    "en": {
        "eyebrow": "SPEAKING PRACTICE",
        "title": "Which exam are you preparing for?",
        "subtitle": "Choose an exam format. You can change the task type on the next screen.",
        "toefl_badge": "CURRENT 2026 FORMAT",
        "toefl_desc": "The new speaking experience focused on academic life.",
        "toefl_one": "7 × Listen and Repeat",
        "toefl_two": "4 × Interview Questions",
        "toefl_btn": "Start TOEFL practice",
        "det_badge": "CURRENT DET FORMAT",
        "det_desc": "Short, visual and interactive speaking tasks.",
        "det_one": "Photo • Reading • Interaction",
        "det_two": "Speaking Sample",
        "det_btn": "Start DET practice",
        "free": "Open freestyle speaking",
        "language": "Interface language",
    },
}


class SelectorScreen(QWidget):
    exam_selected = pyqtSignal(str)
    language_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.language = "tr"
        self._init_ui()
        self._apply_language()

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(54, 32, 54, 32)
        root.setSpacing(0)

        language_bar = QHBoxLayout()
        language_bar.addStretch()
        self.language_label = QLabel()
        self.language_label.setStyleSheet("color:#68758a; font-size:12px; background:transparent;")
        self.language_switch = LanguageSwitch()
        self.language_switch.language_changed.connect(self.set_language)
        language_bar.addWidget(self.language_label)
        language_bar.addSpacing(10)
        language_bar.addWidget(self.language_switch)
        root.addLayout(language_bar)

        root.addStretch(1)
        self.eyebrow = QLabel()
        self.eyebrow.setAlignment(Qt.AlignCenter)
        self.eyebrow.setStyleSheet("color:#2457a6; font-size:12px; font-weight:800; letter-spacing:2px; background:transparent;")
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color:#172033; font-size:32px; font-weight:800; background:transparent;")
        self.subtitle = QLabel()
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("color:#68758a; font-size:14px; background:transparent;")
        root.addWidget(self.eyebrow)
        root.addSpacing(10)
        root.addWidget(self.title)
        root.addSpacing(8)
        root.addWidget(self.subtitle)
        root.addSpacing(34)

        cards = QHBoxLayout()
        cards.setSpacing(22)
        cards.addStretch()
        self.toefl_card = self._create_exam_card("TOEFL iBT", "toefl", "#2457a6", "#edf3fc")
        self.det_card = self._create_exam_card("Duolingo English Test", "det", "#087f6b", "#eaf8f4")
        cards.addWidget(self.toefl_card)
        cards.addWidget(self.det_card)
        cards.addStretch()
        root.addLayout(cards)

        root.addSpacing(22)
        self.free_btn = QPushButton()
        self.free_btn.setCursor(Qt.PointingHandCursor)
        self.free_btn.setFixedWidth(260)
        self.free_btn.setStyleSheet("QPushButton{background:transparent;border:0;color:#68758a;} QPushButton:hover{color:#2457a6;}")
        self.free_btn.clicked.connect(lambda: self.exam_selected.emit("free"))
        root.addWidget(self.free_btn, alignment=Qt.AlignCenter)
        root.addStretch(1)

    def _create_exam_card(self, name, key, accent, tint):
        card = QFrame()
        card.setObjectName(f"{key}Card")
        card.setFixedSize(420, 280)
        card.setStyleSheet(f"""
            QFrame#{key}Card {{ background:#ffffff; border:1px solid #dfe6ef; border-radius:18px; }}
            QFrame#{key}Card:hover {{ border:2px solid {accent}; }}
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 26, 28, 24)
        layout.setSpacing(10)

        badge = QLabel()
        badge.setObjectName("badge")
        badge.setStyleSheet(f"background:{tint}; color:{accent}; border-radius:6px; padding:5px 9px; font-size:10px; font-weight:800;")
        title = QLabel(name)
        title.setStyleSheet("color:#172033; background:transparent; font-size:22px; font-weight:800;")
        desc = QLabel()
        desc.setObjectName("desc")
        desc.setWordWrap(True)
        desc.setStyleSheet("color:#68758a; background:transparent; font-size:13px;")
        detail = QLabel()
        detail.setObjectName("detail")
        detail.setStyleSheet(f"color:{accent}; background:transparent; font-size:13px; font-weight:700; line-height:1.8;")
        button = QPushButton()
        button.setObjectName("action")
        button.setCursor(Qt.PointingHandCursor)
        button.setMinimumHeight(44)
        button.setStyleSheet(f"QPushButton{{background:{accent};border:0;color:white;font-weight:700;}} QPushButton:hover{{background:#173f7a;}}")
        button.clicked.connect(lambda: self.exam_selected.emit(key))

        layout.addWidget(badge, alignment=Qt.AlignLeft)
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addWidget(detail)
        layout.addStretch()
        layout.addWidget(button)
        return card

    def set_language(self, language):
        self.language = "en" if language == "en" else "tr"
        self.language_switch.set_language(self.language)
        self._apply_language()
        self.language_changed.emit(self.language)

    def set_language_silent(self, language):
        self.language = "en" if language == "en" else "tr"
        self.language_switch.set_language(self.language)
        self._apply_language()

    def _apply_language(self):
        t = TEXT[self.language]
        self.eyebrow.setText(t["eyebrow"])
        self.title.setText(t["title"])
        self.subtitle.setText(t["subtitle"])
        self.language_label.setText(t["language"])
        self.free_btn.setText(t["free"] + "  →")
        self._set_card_text(self.toefl_card, t["toefl_badge"], t["toefl_desc"], t["toefl_one"], t["toefl_two"], t["toefl_btn"])
        self._set_card_text(self.det_card, t["det_badge"], t["det_desc"], t["det_one"], t["det_two"], t["det_btn"])

    @staticmethod
    def _set_card_text(card, badge, desc, first, second, button):
        card.findChild(QLabel, "badge").setText(badge)
        card.findChild(QLabel, "desc").setText(desc)
        card.findChild(QLabel, "detail").setText(f"✓  {first}\n✓  {second}")
        card.findChild(QPushButton, "action").setText(button + "  →")
