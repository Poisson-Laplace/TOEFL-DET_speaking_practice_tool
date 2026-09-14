"""
Modern Dark Theme QSS and Color Palette for the Speaking Practice Studio.
"""

DARK_THEME_QSS = """
/* Global Window & Roots */
QMainWindow {
    background-color: #0b0f19;
}

QStackedWidget {
    background-color: #0b0f19;
}

QWidget {
    background-color: #0b0f19;
    color: #f1f5f9;
    font-family: 'Ubuntu', 'Segoe UI', 'Inter', sans-serif;
    font-size: 14px;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #0b0f19;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #334155;
    min-height: 24px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: #475569;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: #0b0f19;
    height: 8px;
    margin: 0px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background: #334155;
    min-width: 24px;
    border-radius: 4px;
}

/* General Buttons */
QPushButton {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #334155;
    border-color: #475569;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #0f172a;
}

QPushButton:disabled {
    background-color: #151d2f;
    color: #64748b;
    border-color: #1e293b;
}

/* Sliders */
QSlider::groove:horizontal {
    height: 6px;
    background: #1e293b;
    border-radius: 3px;
}
QSlider::sub-page:horizontal {
    background: #3b82f6;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #ffffff;
    border: 2px solid #3b82f6;
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 8px;
}
QSlider::handle:horizontal:hover {
    background: #60a5fa;
    border-color: #93c5fd;
}

/* Table Widget */
QTableWidget {
    background-color: #0b0f19;
    border: 1px solid #1e293b;
    border-radius: 8px;
    gridline-color: #1e293b;
    color: #f1f5f9;
    selection-background-color: #1e3a8a;
    selection-color: #ffffff;
}

QHeaderView::section {
    background-color: #151d2f;
    color: #38bdf8;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 0.5px;
    border: none;
    border-bottom: 1px solid #1e293b;
    padding: 8px;
}

QTableWidget::item {
    color: #f1f5f9;
    padding: 6px;
    border-bottom: 1px solid #151d2f;
}

QTableWidget::item:selected {
    background-color: #1e3a8a;
    color: #ffffff;
}

/* ComboBox */
QComboBox {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 6px 12px;
    color: #f1f5f9;
    font-weight: 500;
}
QComboBox:hover {
    border-color: #475569;
}
QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #151d2f;
    border: 1px solid #334155;
    color: #f1f5f9;
    selection-background-color: #2563eb;
    outline: none;
}

/* Tab Bar */
QTabWidget::pane {
    border: 1px solid #1e293b;
    background: #0b0f19;
    border-radius: 8px;
}
QTabBar::tab {
    background: #151d2f;
    color: #94a3b8;
    padding: 8px 18px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 4px;
    font-weight: 700;
    font-size: 13px;
}
QTabBar::tab:hover {
    color: #cbd5e1;
    background: #1e293b;
}
QTabBar::tab:selected {
    background: #1e293b;
    color: #38bdf8;
    border-bottom: 2px solid #38bdf8;
}
"""
