"""
Studio screen for recording speech, transcribing with word-level timestamps,
and interactively reviewing/listening to specific words at exact seconds.
"""

import os
import html
import json
import random
import re
from difflib import SequenceMatcher
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QTimer, QSettings
from PyQt5.QtGui import QColor, QFont, QPixmap
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QSlider,
    QTabWidget, QTextBrowser, QMessageBox, QFileDialog, QApplication
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from prompts import PROMPTS
from audio_recorder import AudioRecorder, wav_has_speech
from stt_engine import TranscribeWorker
from tts_worker import TTSWorker
from ui.language_switch import LanguageSwitch


UI_TEXT = {
    "tr": {
        "back": "← Sınav seçimi",
        "workspace": "Konuşma çalışması",
        "task": "Görev türü",
        "language": "Arayüz dili",
        "next": "Yeni soru",
        "play": "▶ Oynat",
        "pause": "❚❚ Duraklat",
        "timeline": "Kelime zamanları",
        "karaoke": "Etkileşimli metin",
        "copy": "Metni kopyala",
        "export_txt": "TXT indir",
        "export_json": "JSON kaydet",
        "words": "Kelime",
        "speed": "Hız",
        "duration": "Süre",
        "ready": "Hazır",
        "start_listen": "▶ Dinle ve başla",
        "start_record": "● Kayda başla",
        "ready_listen": "Cümleyi dinlemek için başlayabilirsin.",
        "ready_record": "Hazır olduğunda kaydı başlat.",
        "listening": "Cümle oynatılıyor",
        "listening_detail": "Dikkatle dinle; bittiğinde mikrofon otomatik açılacak.",
        "recording": "Kayıt devam ediyor",
        "stop": "■ Kaydı bitir",
        "remaining": "Kayıt {seconds} saniye sonra otomatik bitecek.",
        "processing": "Kayıt hazırlanıyor",
        "processing_detail": "Ses dosyası işleniyor…",
        "completed": "Tamamlandı",
        "analyzing": "Konuşma analiz ediliyor…",
        "analyzing_detail": "Kelimeler ve zaman damgaları çıkarılıyor.",
        "transcript_ready": "Transkripsiyon hazır",
        "detected": "{count} kelime bulundu. Bir kelimeye tıklayarak o noktadan dinleyebilirsin.",
        "empty": "Henüz transkripsiyon yok. Bir yanıt kaydettiğinde burada görünecek.",
        "instruction": "YÖNERGE",
        "prep": "Hazırlık süresi",
        "prep_detail": "Yanıtını planla. Kayıt otomatik başlayacak.",
        "preparing": "Hazırlan…",
        "start_now": "● Şimdi başla",
        "no_speech": "Ses algılanmadı",
        "no_speech_detail": "Transkripsiyon başlatılmadı. Hazır olduğunda yeniden deneyebilirsin.",
        "match": "Cümle uyumu",
        "correct": "Doğru",
        "mostly_correct": "Büyük ölçüde doğru",
        "partial": "Kısmen doğru",
        "try_again": "Tekrar dene",
        "photo_credit": "Fotoğraf",
        "level": "SEVİYE",
        "conversation": "KONUŞMA",
        "turn": "TUR {current}/{total}",
    },
    "en": {
        "back": "← Exam selection",
        "workspace": "Speaking practice",
        "task": "Task type",
        "language": "Interface language",
        "next": "New prompt",
        "play": "▶ Play",
        "pause": "❚❚ Pause",
        "timeline": "Word timing",
        "karaoke": "Interactive transcript",
        "copy": "Copy text",
        "export_txt": "Download TXT",
        "export_json": "Save JSON",
        "words": "Words",
        "speed": "Speed",
        "duration": "Duration",
        "ready": "Ready",
        "start_listen": "▶ Listen and start",
        "start_record": "● Start recording",
        "ready_listen": "Start when you are ready to listen to the sentence.",
        "ready_record": "Start recording when you are ready.",
        "listening": "Playing the sentence",
        "listening_detail": "Listen carefully; the microphone will open automatically when it ends.",
        "recording": "Recording in progress",
        "stop": "■ Finish recording",
        "remaining": "Recording will stop automatically in {seconds} seconds.",
        "processing": "Finishing recording",
        "processing_detail": "Processing the audio file…",
        "completed": "Completed",
        "analyzing": "Analyzing your response…",
        "analyzing_detail": "Extracting words and timestamps.",
        "transcript_ready": "Transcript ready",
        "detected": "Found {count} words. Click any word to play from that point.",
        "empty": "No transcript yet. Your response will appear here after recording.",
        "instruction": "INSTRUCTIONS",
        "prep": "Preparation time",
        "prep_detail": "Plan your response. Recording will start automatically.",
        "preparing": "Get ready…",
        "start_now": "● Start now",
        "no_speech": "No speech detected",
        "no_speech_detail": "Transcription was not started. Try again when you are ready.",
        "match": "Sentence match",
        "correct": "Correct",
        "mostly_correct": "Mostly correct",
        "partial": "Partly correct",
        "try_again": "Try again",
        "photo_credit": "Photo",
        "level": "LEVEL",
        "conversation": "CONVERSATION",
        "turn": "TURN {current}/{total}",
    },
}

TASK_NAMES_TR = {
    "Listen & Repeat": "Dinle ve Tekrar Et",
    "Take an Interview": "Mülakat",
    "Speak About the Photo": "Fotoğraf Hakkında Konuş",
    "Read, Then Speak": "Oku, Sonra Konuş",
    "Interactive Speaking": "Etkileşimli Konuşma",
    "Speaking Sample": "Konuşma Örneği",
    "Free Topic": "Serbest Konu",
}

def format_seconds(seconds: float) -> str:
    """Format float seconds to MM:SS.ss"""
    mins = int(seconds // 60)
    secs = seconds % 60
    return f"{mins:02d}:{secs:05.2f}"

class AppState:
    READY = "READY"
    PREPARING = "PREPARING"
    PLAYING_STIMULUS = "PLAYING_STIMULUS"
    RECORDING_RESPONSE = "RECORDING_RESPONSE"
    FEEDBACK = "FEEDBACK"


class CoverImageLabel(QLabel):
    """Displays a pixmap as a centered, non-distorted cover image."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._source = QPixmap()
        self.setFixedSize(600, 400)
        self.setAlignment(Qt.AlignCenter)

    def set_photo(self, path):
        self._source = QPixmap(path)
        self._update_scaled_pixmap()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_scaled_pixmap()

    def _update_scaled_pixmap(self):
        if self._source.isNull() or self.width() < 2 or self.height() < 2:
            return
        self.setPixmap(self._source.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


class StudioScreen(QWidget):
    """
    Main studio for recording, audio playback, and word-level timestamp inspection.
    """
    back_to_selector = pyqtSignal()
    language_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #f4f7fb;")
        self.language = "tr"
        self.current_exam = "toefl"
        self.current_task_idx = 0
        self.current_prompt = ""
        self.current_scenario_name = ""
        self.current_time_limit = None
        self.current_prep_time = 0
        self.prep_remaining = 0
        self.current_scenario_idx = 0
        self.current_sentence_idx = 0
        self.current_words_data = []
        self.current_audio_path = None
        self.active_word_id = None
        
        self.current_state = AppState.READY
        self.tts_thread = None
        self.stimulus_audio_path = None
        self.current_photo = None
        self.current_difficulty = None
        self.current_conversation = None
        self.current_conversation_topic = ""
        self.current_turn_idx = -1
        self.settings = QSettings("SpeakingPractice", "TOEFLDETTool")
        self.difficulty_progress = {}
        self.flow_id = 0

        self.prep_timer = QTimer(self)
        self.prep_timer.setInterval(1000)
        self.prep_timer.timeout.connect(self._on_prep_tick)

        # Core Engines
        self.recorder = AudioRecorder(self)
        self.recorder.tick.connect(self._on_recorder_tick)
        self.recorder.finished.connect(self._on_recording_finished)
        self.recorder.error.connect(self._on_recorder_error)

        self.transcriber_thread = None

        # Media Player
        self.player = QMediaPlayer(self)
        self.player.positionChanged.connect(self._on_player_position_changed)
        self.player.durationChanged.connect(self._on_player_duration_changed)
        self.player.stateChanged.connect(self._on_player_state_changed)
        
        self.stimulus_player = QMediaPlayer(self)
        self.stimulus_player.mediaStatusChanged.connect(self._on_stimulus_media_status_changed)

        self._init_ui()

    def set_exam(self, exam_key: str):
        """Set active exam mode ('toefl', 'det', 'free') and load tasks."""
        self._cancel_current_flow()
        self.current_exam = exam_key
        exam_info = PROMPTS.get(exam_key, PROMPTS["free"])

        # Update Badge
        self.badge_label.setText(f"[ {exam_info['badge']} ]")
        if exam_key == "toefl":
            self.badge_label.setStyleSheet("""
                background-color: #e8f0fc;
                color: #2457a6;
                border: 1px solid #b9cceb;
                border-radius: 6px;
                padding: 6px 14px;
                font-size: 13px;
                font-weight: 700;
            """)
        elif exam_key == "det":
            self.badge_label.setStyleSheet("""
                background-color: #e7f7f2;
                color: #087f6b;
                border: 1px solid #a9decf;
                border-radius: 6px;
                padding: 6px 14px;
                font-size: 13px;
                font-weight: 700;
            """)
        else:
            self.badge_label.setStyleSheet("""
                background-color: #f1ecfb;
                color: #7047a8;
                border: 1px solid #d4c4eb;
                border-radius: 6px;
                padding: 6px 14px;
                font-size: 13px;
                font-weight: 700;
            """)

        # Populate Task Combo
        self.task_combo.blockSignals(True)
        self.task_combo.clear()
        for task in exam_info["tasks"]:
            self.task_combo.addItem(self._task_display(task))
        self.task_combo.blockSignals(False)

        self.current_task_idx = 0
        self.current_scenario_idx = 0
        self.current_sentence_idx = 0
        self._reset_interactive_conversation()
        self.difficulty_progress[f"{exam_key}/0"] = 0
        self._load_new_prompt()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 16, 28, 18)
        main_layout.setSpacing(9)
        main_layout.setAlignment(Qt.AlignTop)

        # ---------------- TOP NAVIGATION BAR ----------------
        top_bar = QHBoxLayout()
        top_bar.setSpacing(12)

        self.back_btn = QPushButton()
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #526176;
                border: 0;
                padding: 8px 16px;
                font-size: 13px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #e9eef5;
                color: #2457a6;
            }
        """)
        self.back_btn.clicked.connect(self._handle_back)

        self.badge_label = QLabel("TOEFL 2026")
        self.instruction_label = QLabel()
        self.instruction_label.setWordWrap(True)
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setStyleSheet(
            "color:#2457a6;font-size:10px;font-weight:800;letter-spacing:0.3px;background:transparent;"
        )

        top_bar.addWidget(self.back_btn)
        top_bar.addWidget(self.badge_label)
        top_bar.addWidget(self.instruction_label, 1)
        self.language_label = QLabel()
        self.language_label.setStyleSheet("color:#68758a; font-size:12px; background:transparent;")
        self.language_switch = LanguageSwitch()
        self.language_switch.language_changed.connect(self.set_language)
        top_bar.addWidget(self.language_label)
        top_bar.addWidget(self.language_switch)

        main_layout.addLayout(top_bar)

        workspace_bar = QHBoxLayout()
        self.workspace_title = QLabel()
        self.workspace_title.setStyleSheet("color:#172033; font-size:24px; font-weight:800; background:transparent;")
        self.task_label = QLabel()
        self.task_label.setStyleSheet("color:#68758a; font-size:12px; background:transparent;")
        self.task_combo = QComboBox()
        self.task_combo.activated[int].connect(self._on_task_changed)
        self.task_combo.setMinimumWidth(300)
        self.next_prompt_btn = QPushButton()
        self.next_prompt_btn.setCursor(Qt.PointingHandCursor)
        self.next_prompt_btn.setStyleSheet("""
            QPushButton { background:#087f6b; color:#ffffff; border:0; font-weight:700; }
            QPushButton:hover { background:#066b5a; }
        """)
        self.next_prompt_btn.clicked.connect(self._load_new_prompt)
        workspace_bar.addWidget(self.workspace_title)
        workspace_bar.addStretch()
        workspace_bar.addWidget(self.task_label)
        workspace_bar.addWidget(self.task_combo)
        workspace_bar.addWidget(self.next_prompt_btn)
        main_layout.addLayout(workspace_bar)

        # ---------------- PROMPT CARD ----------------
        self.prompt_card = QFrame()
        self.prompt_card.setObjectName("promptCard")
        self.prompt_card.setStyleSheet("""
            QFrame#promptCard {
                background-color: #ffffff;
                border: 1px solid #dfe6ef;
                border-radius: 12px;
            }
        """)
        prompt_layout = QVBoxLayout(self.prompt_card)
        prompt_layout.setContentsMargins(18, 12, 18, 12)
        prompt_layout.setSpacing(6)

        self.prompt_text_label = QLabel("Prompt metni buraya gelecek...")
        self.prompt_text_label.setWordWrap(True)
        self.prompt_text_label.setStyleSheet("color: #172033; font-size: 16px; font-weight: 600; line-height: 1.5; background:transparent;")
        self.prompt_text_label.setAlignment(Qt.AlignCenter)

        self.photo_frame = QFrame()
        self.photo_frame.setObjectName("photoFrame")
        self.photo_frame.setFixedWidth(600)
        self.photo_frame.setStyleSheet("QFrame#photoFrame{background:#eef2f7;border:0;border-radius:10px;}")
        photo_layout = QVBoxLayout(self.photo_frame)
        photo_layout.setContentsMargins(0, 0, 0, 0)
        photo_layout.setSpacing(0)
        self.photo_label = CoverImageLabel()
        self.photo_label.setStyleSheet("background:#e8edf4;border:0;border-radius:10px;")
        self.photo_credit_label = QLabel()
        self.photo_credit_label.setOpenExternalLinks(True)
        self.photo_credit_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.photo_credit_label.setStyleSheet("background:#172033;color:#ffffff;padding:5px 9px;font-size:10px;")
        self.photo_credit_label.setFixedHeight(30)
        photo_layout.addWidget(self.photo_label)
        photo_layout.addWidget(self.photo_credit_label)
        self.photo_frame.setVisible(False)
        prompt_layout.addWidget(self.photo_frame, alignment=Qt.AlignCenter)
        prompt_layout.addWidget(self.prompt_text_label)
        main_layout.addWidget(self.prompt_card)

        # ---------------- RECORDING & STATUS CONSOLE ----------------
        self.control_card = QFrame()
        self.control_card.setObjectName("controlCard")
        self.control_card.setMaximumHeight(112)
        self.control_card.setStyleSheet("""
            QFrame#controlCard {
                background-color: #ffffff;
                border: 1px solid #dfe6ef;
                border-radius: 12px;
            }
        """)
        control_layout = QHBoxLayout(self.control_card)
        control_layout.setContentsMargins(18, 12, 18, 12)
        control_layout.setSpacing(16)

        # Big Timer
        self.timer_label = QLabel("00:00")
        self.timer_label.setStyleSheet("""
            font-size: 32px;
            font-weight: 800;
            color: #173f7a;
            font-family: 'Courier New', monospace;
            background-color: #edf3fc;
            border: 1px solid #cbd9ed;
            border-radius: 10px;
            padding: 4px 16px;
        """)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setFixedSize(132, 70)

        # Record Button
        self.record_btn = QPushButton("▶ Dinle ve Başla")
        self.record_btn.setCursor(Qt.PointingHandCursor)
        self.record_btn.setFixedSize(205, 48)
        self.record_btn.clicked.connect(self._handle_main_action)

        # Status & Info
        status_layout = QVBoxLayout()
        status_layout.setSpacing(4)
        self.status_title = QLabel()
        self.status_title.setStyleSheet("color: #2457a6; font-size: 15px; font-weight: 700; background:transparent;")
        self.status_detail = QLabel()
        self.status_detail.setWordWrap(True)
        self.status_detail.setMinimumWidth(290)
        self.status_detail.setStyleSheet("color: #68758a; font-size: 13px; background:transparent;")
        status_layout.addWidget(self.status_title)
        status_layout.addWidget(self.status_detail)

        control_layout.addStretch()
        control_layout.addWidget(self.timer_label)
        control_layout.addWidget(self.record_btn)
        control_layout.addLayout(status_layout)
        control_layout.addStretch()

        main_layout.addWidget(self.control_card)

        # ---------------- RESULTS & AUDIO PLAYER SECTION ----------------
        self.results_card = QFrame()
        self.results_card.setObjectName("resultsCard")
        self.results_card.setStyleSheet("""
            QFrame#resultsCard {
                background-color: #ffffff;
                border: 1px solid #dfe6ef;
                border-radius: 12px;
            }
        """)
        results_layout = QVBoxLayout(self.results_card)
        results_layout.setContentsMargins(14, 12, 14, 12)
        results_layout.setSpacing(8)

        # Top Audio Player Bar
        player_bar = QHBoxLayout()
        player_bar.setSpacing(14)

        self.play_btn = QPushButton()
        self.play_btn.setCursor(Qt.PointingHandCursor)
        self.play_btn.setFixedWidth(100)
        self.play_btn.setStyleSheet("""
            QPushButton {
                background-color: #2457a6;
                border: 0;
                color: #ffffff;
                font-weight: 700;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #173f7a;
            }
        """)
        self.play_btn.clicked.connect(self._toggle_play)

        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setRange(0, 0)
        self.seek_slider.sliderMoved.connect(self._on_slider_moved)

        self.audio_time_label = QLabel("00:00 / 00:00")
        self.audio_time_label.setStyleSheet("color: #68758a; font-family: monospace; font-size: 13px; min-width: 110px; background:transparent;")

        # Metrics Pills
        self.metrics_label = QLabel("Kelime: 0  |  Hız: 0 WPM  |  Süre: 0.0s")
        self.metrics_label.setStyleSheet("""
            background-color: #edf3fc;
            color: #2457a6;
            border: 1px solid #cbd9ed;
            border-radius: 6px;
            padding: 6px 14px;
            font-size: 13px;
            font-weight: 700;
        """)

        player_bar.addWidget(self.play_btn)
        player_bar.addWidget(self.seek_slider)
        player_bar.addWidget(self.audio_time_label)
        player_bar.addWidget(self.metrics_label)

        results_layout.addLayout(player_bar)

        self.accuracy_label = QLabel()
        self.accuracy_label.setAlignment(Qt.AlignCenter)
        self.accuracy_label.setStyleSheet("background:#eaf8f4;color:#087f6b;border:1px solid #a9decf;border-radius:8px;padding:9px;font-size:14px;font-weight:800;")
        self.accuracy_label.setVisible(False)
        results_layout.addWidget(self.accuracy_label)

        # Dual Tab View (Word Timeline Table vs. Karaoke Flow View)
        self.tab_widget = QTabWidget()

        # Tab 1: Word Timeline Table
        self.table = QTableWidget(0, 5)
        self.table.setMinimumHeight(205)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.cellClicked.connect(self._on_table_cell_clicked)
        self.table.setCursor(Qt.PointingHandCursor)

        self.tab_widget.addTab(self.table, "")

        # Tab 2: Karaoke Reading View
        self.karaoke_view = QTextBrowser()
        self.karaoke_view.setOpenExternalLinks(False)
        self.karaoke_view.anchorClicked.connect(self._on_karaoke_anchor_clicked)
        self.karaoke_view.setStyleSheet("""
            QTextBrowser {
                background-color: #ffffff;
                border: 0;
                border-radius: 8px;
                padding: 18px;
                color: #172033;
                font-size: 16px;
                line-height: 2.2;
            }
        """)
        self.tab_widget.addTab(self.karaoke_view, "")
        self.tab_widget.setMinimumHeight(255)

        results_layout.addWidget(self.tab_widget)

        # Bottom Action Buttons
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        self.copy_btn = QPushButton()
        self.copy_btn.setCursor(Qt.PointingHandCursor)
        self.copy_btn.clicked.connect(self._copy_text)

        self.export_txt_btn = QPushButton()
        self.export_txt_btn.setCursor(Qt.PointingHandCursor)
        self.export_txt_btn.clicked.connect(self._export_txt)

        self.export_json_btn = QPushButton()
        self.export_json_btn.setCursor(Qt.PointingHandCursor)
        self.export_json_btn.clicked.connect(self._export_json)

        actions_layout.addStretch()
        actions_layout.addWidget(self.copy_btn)
        actions_layout.addWidget(self.export_txt_btn)
        actions_layout.addWidget(self.export_json_btn)

        results_layout.addLayout(actions_layout)

        main_layout.addWidget(self.results_card)
        main_layout.setStretchFactor(self.results_card, 1)
        self._apply_language()

    def _text(self, key, **values):
        return UI_TEXT[self.language][key].format(**values)

    def _task_display(self, task):
        name = TASK_NAMES_TR.get(task["type"], task["type"]) if self.language == "tr" else task["type"]
        return name

    def set_language(self, language, emit=True):
        self.language = "en" if language == "en" else "tr"
        if hasattr(self, "language_switch"):
            self.language_switch.set_language(self.language)
        self._apply_language()

        exam_info = PROMPTS.get(self.current_exam, PROMPTS["free"])
        if hasattr(self, "task_combo") and self.task_combo.count():
            selected = self.current_task_idx
            self.task_combo.blockSignals(True)
            self.task_combo.clear()
            for task in exam_info["tasks"]:
                self.task_combo.addItem(self._task_display(task))
            self.task_combo.setCurrentIndex(selected)
            self.task_combo.blockSignals(False)
            self._refresh_instruction()
        self._display_prompt_media()
        self._set_state(self.current_state)
        if emit:
            self.language_changed.emit(self.language)

    def _apply_language(self):
        if not hasattr(self, "back_btn"):
            return
        self.back_btn.setText(self._text("back"))
        self.workspace_title.setText(self._text("workspace"))
        self.task_label.setText(self._text("task"))
        self.language_label.setText(self._text("language"))
        self.next_prompt_btn.setText(self._text("next") + "  ↻")
        self.play_btn.setText(self._text("play"))
        self.tab_widget.setTabText(0, self._text("timeline"))
        self.tab_widget.setTabText(1, self._text("karaoke"))
        self.copy_btn.setText(self._text("copy"))
        self.export_txt_btn.setText(self._text("export_txt"))
        self.export_json_btn.setText(self._text("export_json"))
        if self.language == "tr":
            headers = ["#", "ZAMAN", "KELİME", "SÜRE", "DİNLE"]
        else:
            headers = ["#", "TIME", "WORD", "DURATION", "PLAY"]
        self.table.setHorizontalHeaderLabels(headers)

    def _refresh_instruction(self):
        exam_info = PROMPTS.get(self.current_exam, PROMPTS["free"])
        if not exam_info["tasks"] or self.current_task_idx >= len(exam_info["tasks"]):
            return
        task = exam_info["tasks"][self.current_task_idx]
        instruction = task.get("instructions_tr", task["instructions"]) if self.language == "tr" else task["instructions"]
        limit_label = "HEDEF SÜRE" if self.language == "tr" else "TIME LIMIT"
        unit = "SN" if self.language == "tr" else "SEC"
        limit_text = f"  ·  {limit_label}: {self.current_time_limit} {unit}" if self.current_time_limit else ""
        difficulty_text = ""
        if self.current_difficulty:
            current, total = self.current_difficulty
            difficulty_text = f"  ·  {self._text('level')}: {current}/{total}"
        self.instruction_label.setText(f"{instruction.upper()}{limit_text}{difficulty_text}")

    def _set_state(self, state):
        self.current_state = state
        
        if state == AppState.READY:
            self.player.stop()
            self._reset_results()
            self.results_card.setVisible(False)
            self._render_current_prompt()
                
            self.record_btn.setEnabled(True)
            has_audio_stimulus = bool(self.current_scenario_name)
            self.record_btn.setText(self._text("start_listen" if has_audio_stimulus else "start_record"))
            self.record_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2457a6;
                    border: 0;
                    color: #ffffff;
                    font-size: 16px;
                    font-weight: 800;
                    border-radius: 27px;
                    padding: 12px 24px;
                }
                QPushButton:hover {
                    background-color: #173f7a;
                }
            """)
            self.status_title.setText("● " + self._text("ready"))
            self.status_title.setStyleSheet("color: #2457a6; font-size: 15px; font-weight: 700; background:transparent;")
            self.status_detail.setText(self._text("ready_listen" if has_audio_stimulus else "ready_record"))

        elif state == AppState.PREPARING:
            self.player.stop()
            self._reset_results()
            self.results_card.setVisible(False)
            self._render_current_prompt()
            self.record_btn.setEnabled(True)
            self.record_btn.setText(self._text("start_now"))
            self.record_btn.setStyleSheet("""
                QPushButton {
                    background-color:#d97706; border:0; color:#ffffff; font-size:16px;
                    font-weight:800; border-radius:27px; padding:12px 24px;
                }
            """)
            self.status_title.setText("● " + self._text("prep"))
            self.status_title.setStyleSheet("color:#b56a00;font-size:15px;font-weight:700;background:transparent;")
            self.status_detail.setText(self._text("prep_detail"))
            self._show_prep_time()
            
        elif state == AppState.PLAYING_STIMULUS:
            self.record_btn.setEnabled(False)
            self.record_btn.setText("🔊 " + self._text("listening"))
            self.record_btn.setStyleSheet("""
                QPushButton {
                    background-color: #8794a7;
                    border: 0;
                    color: #ffffff;
                    font-size: 16px;
                    font-weight: 800;
                    border-radius: 27px;
                    padding: 12px 24px;
                }
            """)
            self.status_title.setText("🔊 " + self._text("listening"))
            self.status_title.setStyleSheet("color: #b56a00; font-size: 15px; font-weight: 700; background:transparent;")
            self.status_detail.setText(self._text("listening_detail"))
            
        elif state == AppState.RECORDING_RESPONSE:
            self.record_btn.setEnabled(True)
            self.record_btn.setText(self._text("stop"))
            self.record_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc2626;
                    border: 0;
                    color: #ffffff;
                    font-size: 16px;
                    font-weight: 800;
                    border-radius: 27px;
                    padding: 12px 24px;
                }
                QPushButton:hover {
                    background-color: #b91c1c;
                }
            """)
            self.status_title.setText("● " + self._text("recording"))
            self.status_title.setStyleSheet("color: #c52b35; font-size: 15px; font-weight: 700; background:transparent;")
            self.status_detail.setText(self._text("remaining", seconds=self.current_time_limit) if self.current_time_limit else "")
            
        elif state == AppState.FEEDBACK:
            self.results_card.setVisible(True)
            self._render_current_prompt(reveal_target=True)
            
            self.record_btn.setEnabled(False)
            self.record_btn.setText("✓ " + self._text("completed"))
            self.record_btn.setStyleSheet("""
                QPushButton {
                    background-color: #065f46;
                    border: 2px solid #059669;
                    color: #ffffff;
                    font-size: 16px;
                    font-weight: 800;
                    border-radius: 27px;
                    padding: 12px 24px;
                }
            """)

    # ---------------- PROMPT HANDLING ----------------
    def _on_task_changed(self, idx: int):
        if idx >= 0:
            self.current_task_idx = idx
            self.current_scenario_idx = 0
            self.current_sentence_idx = 0
            self._reset_interactive_conversation()
            self.difficulty_progress[f"{self.current_exam}/{idx}"] = 0
            self._load_new_prompt()

    def _reset_interactive_conversation(self):
        self.current_conversation = None
        self.current_conversation_topic = ""
        self.current_turn_idx = -1

    def _load_new_prompt(self):
        self._cancel_current_flow()
        exam_info = PROMPTS.get(self.current_exam, PROMPTS["free"])
        tasks = exam_info["tasks"]
        if not tasks or self.current_task_idx >= len(tasks):
            return

        task = tasks[self.current_task_idx]
        self.current_time_limit = task.get("time_limit", None)
        self.current_prep_time = int(task.get("prep_time", 0) or 0)
        self.current_photo = None
        self.current_difficulty = None
        
        if "scenarios" in task:
            self._reset_interactive_conversation()
            scenarios = task["scenarios"]
            progress_key = f"{self.current_exam}/{self.current_task_idx}"
            progress = self.difficulty_progress.get(progress_key, 0)
            max_level = min(len(item["sentences"]) for item in scenarios)
            difficulty_index = progress % max_level
            candidates = list(enumerate(scenarios))
            last_prompt = self.settings.value(f"last_prompt/{self.current_exam}/{self.current_task_idx}", "")
            filtered = [item for item in candidates if item[1]["sentences"][difficulty_index] != last_prompt]
            self.current_scenario_idx, scenario = random.choice(filtered or candidates)
            self.current_sentence_idx = difficulty_index
            self.current_difficulty = (difficulty_index + 1, max_level)
            self.current_prompt = scenario["sentences"][difficulty_index]
            self.current_scenario_name = scenario["scenario_name"]
            self.difficulty_progress[progress_key] = progress + 1
            self.settings.setValue(f"last_prompt/{self.current_exam}/{self.current_task_idx}", self.current_prompt)
        elif "conversation_sets" in task:
            self.current_scenario_name = ""
            conversation_sets = task["conversation_sets"]
            if (
                self.current_conversation is None
                or self.current_turn_idx + 1 >= len(self.current_conversation["questions"])
            ):
                last_topic_key = f"last_conversation/{self.current_exam}/{self.current_task_idx}"
                last_topic = self.settings.value(last_topic_key, "")
                candidates = [item for item in conversation_sets if item["topic"] != last_topic]
                self.current_conversation = random.choice(candidates or conversation_sets)
                self.current_conversation_topic = self.current_conversation["topic"]
                self.current_turn_idx = 0
                self.settings.setValue(last_topic_key, self.current_conversation_topic)
            else:
                self.current_turn_idx += 1
            self.current_prompt = self.current_conversation["questions"][self.current_turn_idx]
        else:
            self._reset_interactive_conversation()
            self.current_scenario_name = ""
            prompts_list = task.get("prompts", [])
            if prompts_list:
                key = f"last_prompt/{self.current_exam}/{self.current_task_idx}"
                history_key = f"prompt_history/{self.current_exam}/{self.current_task_idx}"
                try:
                    used_prompts = json.loads(self.settings.value(history_key, "[]"))
                except (TypeError, ValueError):
                    used_prompts = []
                candidates = [item for item in prompts_list if self._prompt_value(item) not in used_prompts]
                if not candidates:
                    used_prompts = []
                    last_prompt = self.settings.value(key, "")
                    candidates = [
                        item for item in prompts_list
                        if self._prompt_value(item) != last_prompt
                    ] or list(prompts_list)
                selected = random.choice(candidates or prompts_list)
                self.current_prompt = self._prompt_value(selected)
                used_prompts.append(self.current_prompt)
                self.settings.setValue(key, self.current_prompt)
                self.settings.setValue(history_key, json.dumps(used_prompts))
                if isinstance(selected, dict):
                    self.current_photo = selected
            else:
                self.current_prompt = "İstediğin konuda serbestçe konuşabilirsin."

        self._refresh_instruction()
        self._display_prompt_media()
        if self.current_prep_time:
            self.prep_remaining = self.current_prep_time
            self._set_state(AppState.PREPARING)
            self.prep_timer.start()
        else:
            self._set_state(AppState.READY)

    @staticmethod
    def _prompt_value(item):
        return item.get("prompt", "") if isinstance(item, dict) else item

    def _display_prompt_media(self):
        if self.current_photo:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            image_path = os.path.join(project_root, self.current_photo["image"])
            self.photo_label.set_photo(image_path)
            credit = self.current_photo.get("credit", "Wikimedia Commons")
            source = self.current_photo.get("source", "https://commons.wikimedia.org")
            self.photo_credit_label.setText(
                f'<a href="{source}" style="color:#ffffff;text-decoration:none;">'
                f'{self._text("photo_credit")}: {credit}  ↗</a>'
            )
            self.photo_frame.setVisible(True)
            self.prompt_text_label.setVisible(False)
            self.prompt_card.setMaximumHeight(456)
        else:
            self.photo_frame.setVisible(False)
            self.prompt_text_label.setVisible(True)
            self.prompt_card.setMaximumHeight(105)
            self._render_current_prompt()

    def _render_current_prompt(self, reveal_target=False):
        if self.current_scenario_name:
            if reveal_target:
                target_label = "Hedef cümle" if self.language == "tr" else "Target sentence"
                self.prompt_text_label.setText(
                    f"<span style='color:#087f6b;font-weight:bold;'>{target_label}:</span> "
                    f"<span style='color:#172033;font-weight:700;'>{html.escape(self.current_prompt)}</span>"
                )
            else:
                hidden_label = "Hedef cümle gizli. Yalnızca dinleyeceksin." if self.language == "tr" else "The sentence is hidden. You will only hear it."
                self.prompt_text_label.setText(
                    f"<span style='color:#172033;font-size:18px;font-weight:700;'>🎧 {hidden_label}</span>"
                )
        elif self.current_conversation:
            total = len(self.current_conversation["questions"])
            turn_label = self._text("turn", current=self.current_turn_idx + 1, total=total)
            self.prompt_text_label.setText(
                f"<span style='color:#087f6b;font-size:12px;font-weight:800;'>"
                f"{self._text('conversation')}: {html.escape(self.current_conversation_topic.upper())} · {turn_label}"
                f"</span><br><span style='color:#172033;font-size:17px;font-weight:700;'>"
                f"{html.escape(self.current_prompt)}</span>"
            )
        else:
            self.prompt_text_label.setText(self.current_prompt)

    def _show_prep_time(self):
        mins, secs = divmod(max(0, self.prep_remaining), 60)
        self.timer_label.setText(f"{mins:02d}:{secs:02d}")

    def _on_prep_tick(self):
        self.prep_remaining -= 1
        self._show_prep_time()
        if self.prep_remaining <= 0:
            self.prep_timer.stop()
            self._start_recording_response()

    def _handle_back(self):
        self._cancel_current_flow()
        self.back_to_selector.emit()

    def _cancel_current_flow(self):
        """Invalidate callbacks and stop media/recording when context changes."""
        self.flow_id += 1
        self.prep_timer.stop()
        self.player.stop()
        self.stimulus_player.stop()
        if self.recorder.is_recording:
            self.recorder.stop_recording(discard=True)
        self.current_audio_path = None

    # ---------------- RECORDING & MAIN ACTION ----------------
    def _handle_main_action(self):
        if self.current_state == AppState.PREPARING:
            self.prep_timer.stop()
            self._start_recording_response()

        elif self.current_state == AppState.READY:
            # Note: For non-scenario tasks without TTS, we might just jump to recording
            if self.current_scenario_name:
                self._start_stimulus_flow()
            else:
                self._start_recording_response()
                
        elif self.current_state == AppState.RECORDING_RESPONSE:
            # Manual early stop
            self.record_btn.setEnabled(False)
            self.status_title.setText("● " + self._text("processing"))
            self.status_title.setStyleSheet("color: #b56a00; font-size: 15px; font-weight: 700; background:transparent;")
            self.status_detail.setText(self._text("processing_detail"))
            self.recorder.stop_recording()

    def _start_stimulus_flow(self):
        self._set_state(AppState.PLAYING_STIMULUS)
        flow_id = self.flow_id
        self.tts_thread = TTSWorker(self.current_prompt, self)
        self.tts_thread.finished_signal.connect(
            lambda path, active_flow=flow_id: self._on_tts_finished(path, active_flow)
        )
        self.tts_thread.error_signal.connect(
            lambda message, active_flow=flow_id: self._on_tts_error(message, active_flow)
        )
        self.tts_thread.start()

    def _on_tts_finished(self, audio_path, flow_id):
        if flow_id != self.flow_id or self.current_state != AppState.PLAYING_STIMULUS:
            return
        self.stimulus_audio_path = audio_path
        self.stimulus_player.setMedia(QMediaContent(QUrl.fromLocalFile(audio_path)))
        self.stimulus_player.play()

    def _on_tts_error(self, err_msg, flow_id):
        if flow_id != self.flow_id:
            return
        QMessageBox.warning(self, "TTS Hatası", f"Ses üretilemedi: {err_msg}")
        self._set_state(AppState.READY)

    def _on_stimulus_media_status_changed(self, status):
        if self.current_state == AppState.PLAYING_STIMULUS and status == QMediaPlayer.EndOfMedia:
            self._start_recording_response()

    def _start_recording_response(self):
        self._set_state(AppState.RECORDING_RESPONSE)
        prefix = f"{self.current_exam}_q"
        # current_time_limit is dynamic, default to 10s if missing
        out_file = self.recorder.start_recording(prefix=prefix, max_duration=self.current_time_limit)
        if not out_file:
            self._set_state(AppState.READY)

    def _on_recorder_tick(self, elapsed_seconds: int):
        # Determine remaining time for countdown
        if self.current_time_limit:
            remaining = max(0, self.current_time_limit - elapsed_seconds)
            mins = remaining // 60
            secs = remaining % 60
            self.timer_label.setText(f"{mins:02d}:{secs:02d}")
        else:
            mins = elapsed_seconds // 60
            secs = elapsed_seconds % 60
            self.timer_label.setText(f"{mins:02d}:{secs:02d}")

    def _on_recorder_error(self, err_msg: str):
        self._set_state(AppState.READY)
        QMessageBox.warning(self, "Kayıt Hatası", err_msg)

    def _on_recording_finished(self, wav_path: str, total_duration: int):
        self._set_state(AppState.FEEDBACK)

        self.current_audio_path = wav_path

        # Setup audio player
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(wav_path)))

        if not wav_has_speech(wav_path):
            self.status_title.setText("● " + self._text("no_speech"))
            self.status_title.setStyleSheet("color:#b56a00;font-size:15px;font-weight:700;background:transparent;")
            self.status_detail.setText(self._text("no_speech_detail"))
            self.metrics_label.setText("")
            self._update_accuracy_feedback("")
            return

        # Start Whisper STT in background thread
        self.status_title.setText("● " + self._text("analyzing"))
        self.status_title.setStyleSheet("color: #2457a6; font-size: 15px; font-weight: 700; background:transparent;")
        self.status_detail.setText(self._text("analyzing_detail"))

        flow_id = self.flow_id
        self.transcriber_thread = TranscribeWorker(wav_path, model_name="base.en", parent=self)
        self.transcriber_thread.finished_signal.connect(
            lambda result, active_flow=flow_id: self._on_stt_finished_for_flow(result, active_flow)
        )
        self.transcriber_thread.error_signal.connect(
            lambda message, active_flow=flow_id: self._on_stt_error_for_flow(message, active_flow)
        )
        self.transcriber_thread.start()

    # ---------------- STT RESULTS HANDLING ----------------
    def _on_stt_finished_for_flow(self, result: dict, flow_id: int):
        if flow_id == self.flow_id:
            self._on_stt_finished(result)

    def _on_stt_error_for_flow(self, err_msg: str, flow_id: int):
        if flow_id == self.flow_id:
            self._on_stt_error(err_msg)

    def _on_stt_finished(self, result: dict):
        self.current_words_data = result.get("words", [])
        duration = result.get("duration", 0.0)
        word_count = result.get("word_count", 0)
        wpm = result.get("wpm", 0.0)
        proc_time = result.get("process_time", 0.0)

        self.status_title.setText("● " + self._text("transcript_ready"))
        self.status_title.setStyleSheet("color: #087f6b; font-size: 15px; font-weight: 700; background:transparent;")
        self.status_detail.setText(self._text("detected", count=word_count))

        self.metrics_label.setText(
            f"{self._text('words')}: {word_count}  |  {self._text('speed')}: {wpm} WPM  |  {self._text('duration')}: {duration:.1f}s  |  STT: {proc_time}s"
        )

        self._update_accuracy_feedback(result.get("full_text", ""))

        # Populate Table
        self.table.setRowCount(0)
        for row_idx, w in enumerate(self.current_words_data):
            self.table.insertRow(row_idx)

            id_item = QTableWidgetItem(str(w["id"]))
            id_item.setTextAlignment(Qt.AlignCenter)
            id_item.setForeground(QColor("#748196"))

            time_str = f"{format_seconds(w['start'])} → {format_seconds(w['end'])}"
            time_item = QTableWidgetItem(time_str)
            time_item.setTextAlignment(Qt.AlignCenter)
            time_item.setForeground(QColor("#2457a6"))

            word_item = QTableWidgetItem(w["word"])
            word_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            word_item.setForeground(QColor("#172033"))
            font = QFont()
            font.setBold(True)
            word_item.setFont(font)

            dur_item = QTableWidgetItem(f"{w['duration']:.2f}s")
            dur_item.setTextAlignment(Qt.AlignCenter)
            dur_item.setForeground(QColor("#087f6b"))

            play_item = QTableWidgetItem("▶ Dinle")
            play_item.setTextAlignment(Qt.AlignCenter)
            play_item.setForeground(QColor("#2457a6"))

            self.table.setItem(row_idx, 0, id_item)
            self.table.setItem(row_idx, 1, time_item)
            self.table.setItem(row_idx, 2, word_item)
            self.table.setItem(row_idx, 3, dur_item)
            self.table.setItem(row_idx, 4, play_item)

        # Populate Karaoke Flow View
        self._render_karaoke_view(active_id=None)

    def _update_accuracy_feedback(self, transcript):
        exam_info = PROMPTS.get(self.current_exam, PROMPTS["free"])
        task = exam_info["tasks"][self.current_task_idx]
        if self.current_exam != "toefl" or task.get("type") != "Listen & Repeat":
            self.accuracy_label.setVisible(False)
            return

        normalize = lambda text: re.findall(r"[a-z0-9']+", text.lower())
        target_words = normalize(self.current_prompt)
        spoken_words = normalize(transcript)
        score = round(SequenceMatcher(None, target_words, spoken_words).ratio() * 100) if spoken_words else 0

        if score >= 90:
            result_key, background, color, border = "correct", "#eaf8f4", "#087f6b", "#a9decf"
        elif score >= 75:
            result_key, background, color, border = "mostly_correct", "#eef4fd", "#2457a6", "#bfd0ec"
        elif score >= 50:
            result_key, background, color, border = "partial", "#fff7e8", "#a35b00", "#f2d29a"
        else:
            result_key, background, color, border = "try_again", "#fff0f1", "#b4232e", "#efbbc0"

        self.accuracy_label.setText(
            f"{self._text('match')}: %{score}  ·  {self._text(result_key)}"
        )
        self.accuracy_label.setStyleSheet(
            f"background:{background};color:{color};border:1px solid {border};"
            "border-radius:8px;padding:9px;font-size:14px;font-weight:800;"
        )
        self.accuracy_label.setVisible(True)

    def _on_stt_error(self, err_msg: str):
        self.status_title.setText("● Transkripsiyon Hatası")
        self.status_title.setStyleSheet("color: #ef4444; font-size: 15px; font-weight: 700;")
        self.status_detail.setText(err_msg)
        QMessageBox.warning(self, "STT Hatası", f"Konuşma metne dökülürken hata oluştu: {err_msg}")

    # ---------------- AUDIO PLAYBACK & SYNC ----------------
    def _toggle_play(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def _on_player_state_changed(self, state):
        if state == QMediaPlayer.PlayingState:
            self.play_btn.setText(self._text("pause"))
        else:
            self.play_btn.setText(self._text("play"))

    def _on_player_duration_changed(self, duration_ms: int):
        self.seek_slider.setRange(0, duration_ms)

    def _on_player_position_changed(self, position_ms: int):
        self.seek_slider.blockSignals(True)
        self.seek_slider.setValue(position_ms)
        self.seek_slider.blockSignals(False)

        current_sec = position_ms / 1000.0
        total_sec = self.player.duration() / 1000.0 if self.player.duration() > 0 else 0.0
        self.audio_time_label.setText(f"{format_seconds(current_sec)} / {format_seconds(total_sec)}")

        active_w_id = None
        for w in self.current_words_data:
            if w["start"] <= current_sec <= w["end"] + 0.15:
                active_w_id = w["id"]
                break

        if active_w_id != self.active_word_id:
            self.active_word_id = active_w_id
            self._highlight_active_word(active_w_id)

    def _on_slider_moved(self, position_ms: int):
        self.player.setPosition(position_ms)

    def _seek_to_second(self, seconds: float):
        pos_ms = int(seconds * 1000)
        self.player.setPosition(pos_ms)
        if self.player.state() != QMediaPlayer.PlayingState:
            self.player.play()

    # ---------------- WORD INTERACTION (CLICK TO SEEK) ----------------
    def _on_table_cell_clicked(self, row: int, col: int):
        if 0 <= row < len(self.current_words_data):
            word_obj = self.current_words_data[row]
            self._seek_to_second(word_obj["start"])
            self._render_karaoke_view(active_id=word_obj["id"])

    def _on_karaoke_anchor_clicked(self, url: QUrl):
        anchor = url.toString()
        if anchor.startswith("word:"):
            try:
                w_id = int(anchor.split(":")[1])
                for w in self.current_words_data:
                    if w["id"] == w_id:
                        self._seek_to_second(w["start"])
                        self.table.selectRow(w_id - 1)
                        break
            except Exception:
                pass

    def _highlight_active_word(self, word_id: int or None):
        if word_id is not None and 0 <= (word_id - 1) < self.table.rowCount():
            self.table.selectRow(word_id - 1)
        self._render_karaoke_view(active_id=word_id)

    def _render_karaoke_view(self, active_id: int or None):
        if not self.current_words_data:
            self.karaoke_view.setHtml(f"<p style='color:#748196;'>{self._text('empty')}</p>")
            return

        html_tokens = []
        for w in self.current_words_data:
            w_id = w["id"]
            w_text = w["word"]
            w_time = f"{w['start']:.2f}s"

            if w_id == active_id:
                token = f"""
                <a href="word:{w_id}" style="text-decoration: none;">
                    <span style="background-color:#f6c766;color:#172033;font-weight:800;padding:2px 7px;border-radius:5px;font-size:17px;">{w_text}</span>
                </a>
                """
            else:
                token = f"""
                <a href="word:{w_id}" title="[{w_time}]" style="text-decoration:none;color:#172033;">
                    <span style="padding:2px 5px;border-radius:4px;background-color:#edf2f7;">{w_text}</span>
                </a>
                """
            html_tokens.append(token)

        content = " ".join(html_tokens)
        full_html = f"""
        <html>
        <body style="font-family:'Segoe UI','Ubuntu',sans-serif;line-height:2.2;font-size:15px;color:#172033;background-color:#ffffff;">
            {content}
        </body>
        </html>
        """
        self.karaoke_view.setHtml(full_html)

    # ---------------- EXPORT & ACTIONS ----------------
    def _reset_results(self):
        self.current_words_data = []
        self.active_word_id = None
        self.table.setRowCount(0)
        self.karaoke_view.clear()
        
        # Reset timer display based on limit
        if self.current_time_limit:
            mins = self.current_time_limit // 60
            secs = self.current_time_limit % 60
            self.timer_label.setText(f"{mins:02d}:{secs:02d}")
        else:
            self.timer_label.setText("00:00")
            
        self.audio_time_label.setText("00:00 / 00:00")
        self.seek_slider.setRange(0, 0)
        self.seek_slider.setValue(0)
        self.metrics_label.setText(
            f"{self._text('words')}: 0  |  {self._text('speed')}: 0 WPM  |  {self._text('duration')}: 0.0s"
        )
        self.accuracy_label.setVisible(False)

    def _copy_text(self):
        if not self.current_words_data:
            return
        full_text = " ".join([w["word"] for w in self.current_words_data])
        QApplication.clipboard().setText(full_text)
        QMessageBox.information(self, "Kopyalandı", "Döküm metni panoya kopyalandı!")

    def _export_txt(self):
        if not self.current_words_data:
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Zaman Damgalı TXT Kaydet", "transcript_timestamps.txt", "Text Files (*.txt)")
        if file_path:
            lines = [
                f"Sınav: {self.current_exam.upper()}",
                f"Soru/Prompt: {self.current_prompt}",
                f"Ses Dosyası: {self.current_audio_path}",
                "=" * 60,
                "ZAMAN DAMGALI KELİME DÖKÜMÜ:",
                "=" * 60,
            ]
            for w in self.current_words_data:
                lines.append(f"[{format_seconds(w['start'])} - {format_seconds(w['end'])}] ({w['duration']:.2f}s) : {w['word']}")

            lines.append("=" * 60)
            lines.append("TAM METİN:")
            lines.append(" ".join([w["word"] for w in self.current_words_data]))

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

            QMessageBox.information(self, "Kaydedildi", f"Döküm başarıyla kaydedildi:\n{file_path}")

    def _export_json(self):
        if not self.current_words_data:
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "JSON Kaydet", "transcript_data.json", "JSON Files (*.json)")
        if file_path:
            data = {
                "exam": self.current_exam,
                "prompt": self.current_prompt,
                "audio_path": self.current_audio_path,
                "full_text": " ".join([w["word"] for w in self.current_words_data]),
                "word_count": len(self.current_words_data),
                "words": self.current_words_data,
            }
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            QMessageBox.information(self, "Kaydedildi", f"JSON verisi kaydedildi:\n{file_path}")
