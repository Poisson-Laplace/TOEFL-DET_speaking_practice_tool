"""Shared light theme for the desktop application."""

DARK_THEME_QSS = """
QMainWindow, QStackedWidget, QWidget {
    background-color: #f4f7fb;
    color: #172033;
    font-family: 'Ubuntu', 'Segoe UI', 'Inter', sans-serif;
    font-size: 14px;
}
QToolTip { background-color: #172033; color: #ffffff; border: 0; padding: 6px; }
QPushButton {
    background-color: #ffffff; color: #24324a; border: 1px solid #d7dfeb;
    border-radius: 9px; padding: 9px 15px; font-weight: 600;
}
QPushButton:hover { background-color: #f8fafc; border-color: #9aacbf; }
QPushButton:pressed { background-color: #eef2f7; }
QPushButton:disabled { background-color: #edf1f5; color: #98a3b3; border-color: #e0e6ee; }
QComboBox {
    background-color: #ffffff; color: #172033; border: 1px solid #d7dfeb;
    border-radius: 9px; padding: 8px 12px; min-height: 20px;
}
QComboBox:hover { border-color: #8fa1b7; }
QComboBox::drop-down { border: 0; width: 28px; }
QComboBox QAbstractItemView {
    background-color: #ffffff; color: #172033; border: 1px solid #d7dfeb;
    selection-background-color: #e7eefb; selection-color: #173f7a; outline: 0;
}
QSlider::groove:horizontal { height: 5px; background: #dfe6ef; border-radius: 2px; }
QSlider::sub-page:horizontal { background: #2457a6; border-radius: 2px; }
QSlider::handle:horizontal {
    background: #ffffff; border: 2px solid #2457a6; width: 15px; height: 15px;
    margin: -6px 0; border-radius: 8px;
}
QTableWidget {
    background-color: #ffffff; alternate-background-color: #f8fafc; color: #172033;
    border: 0; gridline-color: #e8edf3; selection-background-color: #e4edfb;
    selection-color: #173f7a;
}
QHeaderView::section {
    background-color: #f4f7fb; color: #68758a; border: 0;
    border-bottom: 1px solid #dfe6ef; padding: 9px; font-size: 11px; font-weight: 700;
}
QTableWidget::item { border-bottom: 1px solid #edf1f5; padding: 7px; }
QTabWidget::pane {
    background: #ffffff; border: 1px solid #dfe6ef; border-radius: 9px; top: -1px;
}
QTabBar::tab {
    background: transparent; color: #748196; padding: 9px 16px;
    border-bottom: 2px solid transparent; font-weight: 600;
}
QTabBar::tab:hover { color: #2457a6; }
QTabBar::tab:selected { color: #2457a6; border-bottom-color: #2457a6; }
QScrollBar:vertical { border: 0; background: #f1f4f8; width: 9px; margin: 0; }
QScrollBar::handle:vertical { background: #c7d1df; min-height: 28px; border-radius: 4px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
"""
