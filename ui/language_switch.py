"""Compact Turkish/English toggle shared by both screens."""

from PyQt5.QtCore import Qt, pyqtSignal, QRectF
from PyQt5.QtGui import QColor, QFont, QPainter
from PyQt5.QtWidgets import QAbstractButton


class LanguageSwitch(QAbstractButton):
    language_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._language = "tr"
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(116, 36)
        self.setToolTip("Türkçe / English")
        self.clicked.connect(self._toggle_language)

    @property
    def language(self):
        return self._language

    def set_language(self, language, emit=False):
        language = "en" if language == "en" else "tr"
        if language == self._language:
            return
        self._language = language
        self.setChecked(language == "en")
        self.update()
        if emit:
            self.language_changed.emit(language)

    def _toggle_language(self):
        self._language = "en" if self.isChecked() else "tr"
        self.language_changed.emit(self._language)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor("#d3dce8"))
        painter.setBrush(QColor("#edf2f7"))
        painter.drawRoundedRect(QRectF(0.5, 0.5, self.width() - 1, self.height() - 1), 18, 18)

        active_x = self.width() / 2 if self._language == "en" else 2
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#2457a6"))
        painter.drawRoundedRect(QRectF(active_x, 2, self.width() / 2 - 2, self.height() - 4), 16, 16)

        font = QFont(self.font())
        font.setPointSize(9)
        font.setBold(True)
        painter.setFont(font)
        for index, label in enumerate(("TR", "EN")):
            rect = QRectF(index * self.width() / 2, 0, self.width() / 2, self.height())
            is_active = (index == 0 and self._language == "tr") or (index == 1 and self._language == "en")
            painter.setPen(QColor("#ffffff") if is_active else QColor("#718096"))
            painter.drawText(rect, Qt.AlignCenter, label)
