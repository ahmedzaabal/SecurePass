"""
Modern styling for SecurePass
"""

class Styles:
    """Application styles and themes"""
    
    @staticmethod
    def get_dark_theme():
        return """
        * {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
            font-size: 9pt;
        }
        
        QMainWindow {
            background-color: #0f0f0f;
        }
        
        QWidget {
            background-color: #0f0f0f;
            color: #e4e4e7;
        }
        
        QMenuBar {
            background-color: #18181b;
            color: #e4e4e7;
            border: none;
            border-bottom: 1px solid #27272a;
            padding: 4px;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 6px 12px;
            border-radius: 6px;
        }
        
        QMenuBar::item:selected {
            background-color: #27272a;
        }
        
        QMenu {
            background-color: #18181b;
            color: #e4e4e7;
            border: 1px solid #27272a;
            border-radius: 8px;
            padding: 4px;
        }
        
        QMenu::item {
            padding: 8px 32px 8px 12px;
            border-radius: 6px;
        }
        
        QMenu::item:selected {
            background-color: #2563eb;
            color: white;
        }
        
        QMenu::separator {
            height: 1px;
            background-color: #27272a;
            margin: 4px 8px;
        }
        
        QStatusBar {
            background-color: #18181b;
            color: #a1a1aa;
            border: none;
            border-top: 1px solid #27272a;
        }
        
        QStatusBar QLabel {
            background-color: transparent;
            padding: 4px 8px;
        }
        
        QSplitter::handle {
            background-color: #27272a;
            width: 1px;
        }
        
        QSplitter::handle:hover {
            background-color: #3f3f46;
        }
        
        QListWidget {
            background-color: #18181b;
            border: 1px solid #27272a;
            border-radius: 10px;
            padding: 4px;
            outline: none;
        }
        
        QListWidget::item {
            background-color: transparent;
            color: #e4e4e7;
            padding: 10px 12px;
            border-radius: 8px;
            margin: 2px 0px;
        }
        
        QListWidget::item:hover {
            background-color: #27272a;
        }
        
        QListWidget::item:selected {
            background-color: #2563eb;
            color: white;
        }
        
        QLineEdit {
            background-color: #18181b;
            color: #e4e4e7;
            border: 1px solid #27272a;
            border-radius: 8px;
            padding: 8px 12px;
            selection-background-color: #2563eb;
        }
        
        QLineEdit:hover {
            border: 1px solid #3f3f46;
        }
        
        QLineEdit:focus {
            border: 1px solid #2563eb;
            outline: none;
        }
        
        QTextEdit {
            background-color: #18181b;
            color: #e4e4e7;
            border: 1px solid #27272a;
            border-radius: 8px;
            padding: 8px;
            selection-background-color: #2563eb;
        }
        
        QTextEdit:hover {
            border: 1px solid #3f3f46;
        }
        
        QTextEdit:focus {
            border: 1px solid #2563eb;
        }
        
        QPushButton {
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 500;
        }
        
        QPushButton:hover {
            background-color: #1d4ed8;
        }
        
        QPushButton:pressed {
            background-color: #1e40af;
        }
        
        QPushButton:disabled {
            background-color: #27272a;
            color: #71717a;
        }
        
        QPushButton#secondaryBtn {
            background-color: #27272a;
            color: #e4e4e7;
        }
        
        QPushButton#secondaryBtn:hover {
            background-color: #3f3f46;
        }
        
        QPushButton#secondaryBtn:pressed {
            background-color: #52525b;
        }
        
        QPushButton#dangerBtn {
            background-color: #dc2626;
            color: white;
        }
        
        QPushButton#dangerBtn:hover {
            background-color: #b91c1c;
        }
        
        QPushButton#dangerBtn:pressed {
            background-color: #991b1b;
        }
        
        QDialog {
            background-color: #0f0f0f;
        }
        
        QFormLayout QLabel {
            color: #a1a1aa;
            font-weight: 500;
        }
        
        QSpinBox {
            background-color: #18181b;
            color: #e4e4e7;
            border: 1px solid #27272a;
            border-radius: 8px;
            padding: 6px 12px;
        }
        
        QSpinBox:hover {
            border: 1px solid #3f3f46;
        }
        
        QSpinBox:focus {
            border: 1px solid #2563eb;
        }
        
        QSpinBox::up-button, QSpinBox::down-button {
            background-color: #27272a;
            border: none;
            width: 16px;
        }
        
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background-color: #3f3f46;
        }
        
        QCheckBox {
            color: #e4e4e7;
            spacing: 8px;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 1px solid #3f3f46;
            background-color: #18181b;
        }
        
        QCheckBox::indicator:hover {
            border: 1px solid #52525b;
        }
        
        QCheckBox::indicator:checked {
            background-color: #2563eb;
            border: 1px solid #2563eb;
            image: none;
        }
        
        QProgressBar {
            background-color: #27272a;
            border: none;
            border-radius: 4px;
            height: 8px;
            text-align: center;
        }
        
        QProgressBar::chunk {
            background-color: #2563eb;
            border-radius: 4px;
        }
        
        QLabel#cardTitle {
            color: #ffffff;
            font-size: 11pt;
            font-weight: 600;
        }
        
        QLabel#sectionLabel {
            color: #a1a1aa;
            font-size: 8pt;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        QLabel#detailValue {
            color: #e4e4e7;
            padding: 6px 0px;
        }
        
        QFrame#card {
            background-color: #18181b;
            border: 1px solid #27272a;
            border-radius: 12px;
        }
        
        QFrame#divider {
            background-color: #27272a;
            max-height: 1px;
        }
        """
    
    @staticmethod
    def get_light_theme():
        return """
        * {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
            font-size: 9pt;
        }
        
        QMainWindow {
            background-color: #f9fafb;
        }
        
        QWidget {
            background-color: #f9fafb;
            color: #111827;
        }
        
        QMenuBar {
            background-color: #ffffff;
            color: #111827;
            border: none;
            border-bottom: 1px solid #e5e7eb;
            padding: 4px;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 6px 12px;
            border-radius: 6px;
        }
        
        QMenuBar::item:selected {
            background-color: #f3f4f6;
        }
        
        QMenu {
            background-color: #ffffff;
            color: #111827;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 4px;
        }
        
        QMenu::item {
            padding: 8px 32px 8px 12px;
            border-radius: 6px;
        }
        
        QMenu::item:selected {
            background-color: #2563eb;
            color: white;
        }
        
        QMenu::separator {
            height: 1px;
            background-color: #e5e7eb;
            margin: 4px 8px;
        }
        
        QStatusBar {
            background-color: #ffffff;
            color: #6b7280;
            border: none;
            border-top: 1px solid #e5e7eb;
        }
        
        QStatusBar QLabel {
            background-color: transparent;
            padding: 4px 8px;
        }
        
        QSplitter::handle {
            background-color: #e5e7eb;
            width: 1px;
        }
        
        QSplitter::handle:hover {
            background-color: #d1d5db;
        }
        
        QListWidget {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 4px;
            outline: none;
        }
        
        QListWidget::item {
            background-color: transparent;
            color: #111827;
            padding: 10px 12px;
            border-radius: 8px;
            margin: 2px 0px;
        }
        
        QListWidget::item:hover {
            background-color: #f3f4f6;
        }
        
        QListWidget::item:selected {
            background-color: #2563eb;
            color: white;
        }
        
        QLineEdit {
            background-color: #ffffff;
            color: #111827;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 8px 12px;
            selection-background-color: #2563eb;
        }
        
        QLineEdit:hover {
            border: 1px solid #9ca3af;
        }
        
        QLineEdit:focus {
            border: 1px solid #2563eb;
            outline: none;
        }
        
        QTextEdit {
            background-color: #ffffff;
            color: #111827;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 8px;
            selection-background-color: #2563eb;
        }
        
        QTextEdit:hover {
            border: 1px solid #9ca3af;
        }
        
        QTextEdit:focus {
            border: 1px solid #2563eb;
        }
        
        QPushButton {
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 500;
        }
        
        QPushButton:hover {
            background-color: #1d4ed8;
        }
        
        QPushButton:pressed {
            background-color: #1e40af;
        }
        
        QPushButton:disabled {
            background-color: #f3f4f6;
            color: #9ca3af;
        }
        
        QPushButton#secondaryBtn {
            background-color: #f3f4f6;
            color: #111827;
            border: 1px solid #d1d5db;
        }
        
        QPushButton#secondaryBtn:hover {
            background-color: #e5e7eb;
        }
        
        QPushButton#secondaryBtn:pressed {
            background-color: #d1d5db;
        }
        
        QPushButton#dangerBtn {
            background-color: #dc2626;
            color: white;
        }
        
        QPushButton#dangerBtn:hover {
            background-color: #b91c1c;
        }
        
        QPushButton#dangerBtn:pressed {
            background-color: #991b1b;
        }
        
        QDialog {
            background-color: #f9fafb;
        }
        
        QFormLayout QLabel {
            color: #374151;
            font-weight: 500;
        }
        
        QSpinBox {
            background-color: #ffffff;
            color: #111827;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 6px 12px;
        }
        
        QSpinBox:hover {
            border: 1px solid #9ca3af;
        }
        
        QSpinBox:focus {
            border: 1px solid #2563eb;
        }
        
        QSpinBox::up-button, QSpinBox::down-button {
            background-color: #f3f4f6;
            border: none;
            width: 16px;
        }
        
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background-color: #e5e7eb;
        }
        
        QCheckBox {
            color: #111827;
            spacing: 8px;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 1px solid #d1d5db;
            background-color: #ffffff;
        }
        
        QCheckBox::indicator:hover {
            border: 1px solid #9ca3af;
        }
        
        QCheckBox::indicator:checked {
            background-color: #2563eb;
            border: 1px solid #2563eb;
        }
        
        QLabel#cardTitle {
            color: #111827;
            font-size: 11pt;
            font-weight: 600;
        }
        
        QLabel#sectionLabel {
            color: #6b7280;
            font-size: 8pt;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        QLabel#detailValue {
            color: #111827;
            padding: 6px 0px;
        }
        
        QFrame#card {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
        }
        
        QFrame#divider {
            background-color: #e5e7eb;
            max-height: 1px;
        }
        """
    
    @staticmethod
    def apply(app, theme='dark'):
        if theme == 'dark':
            app.setStyleSheet(Styles.get_dark_theme())
        else:
            app.setStyleSheet(Styles.get_light_theme())
