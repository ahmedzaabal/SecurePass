"""
Main window for SecurePass
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QListWidget, QListWidgetItem, QPushButton,
                             QLabel, QLineEdit, QTextEdit, QMessageBox,
                             QMenuBar, QMenu, QStatusBar, QSplitter,
                             QDialog, QFormLayout, QDialogButtonBox,
                             QSpinBox, QCheckBox, QProgressBar, QFrame,
                             QScrollArea)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QIcon, QFont
import pyperclip
import time

from core.vault import Vault
from ui.lock_screen import LockScreen
from ui.styles import Styles
from utils.password_generator import PasswordGenerator

class AddEditDialog(QDialog):
    """Dialog for adding or editing entries"""
    
    def __init__(self, parent=None, entry=None):
        super().__init__(parent)
        self.entry = entry
        self.generator = PasswordGenerator()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Add Entry" if self.entry is None else "Edit Entry")
        self.setMinimumWidth(450)
        self.setMinimumHeight(500)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("Add New Entry" if self.entry is None else "Edit Entry")
        title.setObjectName("cardTitle")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("e.g., Google, GitHub")
        self.title_input.setMinimumHeight(40)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Email or username")
        self.username_input.setMinimumHeight(40)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setMinimumHeight(40)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        self.url_input.setMinimumHeight(40)
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Additional notes...")
        self.notes_input.setMinimumHeight(80)
        
        if self.entry:
            self.title_input.setText(self.entry.get('title', ''))
            self.username_input.setText(self.entry.get('username', ''))
            self.password_input.setText(self.entry.get('password', ''))
            self.url_input.setText(self.entry.get('url', ''))
            self.notes_input.setPlainText(self.entry.get('notes', ''))
        
        form_layout.addRow("Title", self.title_input)
        form_layout.addRow("Username/Email", self.username_input)
        form_layout.addRow("Password", self.password_input)
        form_layout.addRow("URL", self.url_input)
        form_layout.addRow("Notes", self.notes_input)
        
        layout.addLayout(form_layout)
        
        # Password generator
        gen_layout = QHBoxLayout()
        gen_layout.setSpacing(8)
        self.gen_btn = QPushButton("🎲 Generate Password")
        self.gen_btn.setObjectName("secondaryBtn")
        self.gen_btn.clicked.connect(self.generate_password)
        self.show_btn = QPushButton("👁 Show/Hide")
        self.show_btn.setObjectName("secondaryBtn")
        self.show_btn.clicked.connect(self.toggle_password)
        gen_layout.addWidget(self.gen_btn)
        gen_layout.addWidget(self.show_btn)
        gen_layout.addStretch()
        layout.addLayout(gen_layout)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondaryBtn")
        cancel_btn.clicked.connect(self.reject)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def generate_password(self):
        pwd = self.generator.generate(16)
        self.password_input.setText(pwd)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
    
    def toggle_password(self):
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
    
    def get_data(self):
        return {
            'title': self.title_input.text(),
            'username': self.username_input.text(),
            'password': self.password_input.text(),
            'url': self.url_input.text(),
            'notes': self.notes_input.toPlainText()
        }

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.vault = Vault()
        self.generator = PasswordGenerator()
        self.current_entry_id = None
        self.lock_timer = QTimer()
        self.lock_timer.timeout.connect(self.auto_lock)
        self.inactivity_timeout = 300000  # 5 minutes
        self.last_activity = time.time()
        
        self.init_ui()
        self.show_lock_screen()
    
    def init_ui(self):
        self.setWindowTitle("SecurePass")
        self.setMinimumSize(900, 650)
        
        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        
        lock_action = QAction("🔒 &Lock Vault", self)
        lock_action.setShortcut("Ctrl+L")
        lock_action.triggered.connect(self.lock_vault)
        file_menu.addAction(lock_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        edit_menu = menubar.addMenu("&Edit")
        add_action = QAction("➕ &Add Entry", self)
        add_action.setShortcut("Ctrl+N")
        add_action.triggered.connect(self.add_entry)
        edit_menu.addAction(add_action)
        
        tools_menu = menubar.addMenu("&Tools")
        gen_action = QAction("🎲 &Password Generator", self)
        gen_action.triggered.connect(self.show_password_generator)
        tools_menu.addAction(gen_action)
        
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.status_label = QLabel("🔒 Locked")
        self.statusBar.addWidget(self.status_label)
    
    def show_lock_screen(self):
        """Show lock/unlock screen"""
        self.clear_main_area()
        lock_screen = LockScreen(vault_exists=self.vault.vault_exists())
        lock_screen.unlocked.connect(self.on_unlocked)
        self.main_layout.addWidget(lock_screen)
        self.lock_screen = lock_screen
    
    def clear_main_area(self):
        """Clear all widgets from main area"""
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def on_unlocked(self, master_password):
        """Handle vault unlock/create"""
        if self.vault.vault_exists():
            success = self.vault.unlock_vault(master_password)
            if not success:
                QMessageBox.critical(self, "Error", "Invalid master password")
                return
        else:
            success = self.vault.create_vault(master_password)
            if not success:
                QMessageBox.critical(self, "Error", "Failed to create vault")
                return
        
        self.master_password = master_password
        self.clear_main_area()
        self.setup_main_ui()
        self.status_label.setText(f"🔓 Unlocked • {len(self.vault.get_entries())} entries")
        self.start_inactivity_timer()
    
    def setup_main_ui(self):
        """Setup main UI when vault is unlocked"""
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(12, 12, 12, 12)
        container_layout.setSpacing(12)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(1)
        
        # Left panel - entry list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)
        
        # Header
        left_header = QLabel("My Vault")
        left_header.setObjectName("cardTitle")
        header_font = QFont()
        header_font.setPointSize(12)
        header_font.setBold(True)
        left_header.setFont(header_font)
        left_layout.addWidget(left_header)
        
        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search entries...")
        self.search_input.setMinimumHeight(38)
        self.search_input.textChanged.connect(self.filter_entries)
        left_layout.addWidget(self.search_input)
        
        # Entry list card
        list_card = QFrame()
        list_card.setObjectName("card")
        list_card_layout = QVBoxLayout(list_card)
        list_card_layout.setContentsMargins(6, 6, 6, 6)
        
        self.entry_list = QListWidget()
        self.entry_list.setFrameShape(QListWidget.Shape.NoFrame)
        self.entry_list.itemClicked.connect(self.show_entry_details)
        list_card_layout.addWidget(self.entry_list)
        left_layout.addWidget(list_card)
        
        # Add button
        add_btn = QPushButton("➕ Add Entry")
        add_btn.setMinimumHeight(38)
        add_btn.clicked.connect(self.add_entry)
        left_layout.addWidget(add_btn)
        
        splitter.addWidget(left_widget)
        
        # Right panel - entry details
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)
        
        # Details header
        details_header = QLabel("Entry Details")
        details_header.setObjectName("cardTitle")
        details_header.setFont(header_font)
        right_layout.addWidget(details_header)
        
        # Details card
        details_card = QFrame()
        details_card.setObjectName("card")
        details_card_layout = QVBoxLayout(details_card)
        details_card_layout.setContentsMargins(24, 24, 24, 24)
        details_card_layout.setSpacing(16)
        
        self.detail_title = QLabel("Select an entry to view details")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.detail_title.setFont(title_font)
        self.detail_title.setWordWrap(True)
        details_card_layout.addWidget(self.detail_title)
        
        # Divider
        divider1 = QFrame()
        divider1.setObjectName("divider")
        divider1.setFrameShape(QFrame.Shape.HLine)
        details_card_layout.addWidget(divider1)
        
        # Username section
        user_section = QLabel("USERNAME / EMAIL")
        user_section.setObjectName("sectionLabel")
        details_card_layout.addWidget(user_section)
        self.detail_username = QLabel("")
        self.detail_username.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.detail_username.setWordWrap(True)
        self.detail_username.setStyleSheet("font-size: 10pt;")
        details_card_layout.addWidget(self.detail_username)
        copy_user_btn = QPushButton("Copy Username")
        copy_user_btn.setObjectName("secondaryBtn")
        copy_user_btn.setFixedWidth(150)
        copy_user_btn.clicked.connect(self.copy_username)
        details_card_layout.addWidget(copy_user_btn)
        
        # Password section
        pwd_section = QLabel("PASSWORD")
        pwd_section.setObjectName("sectionLabel")
        details_card_layout.addWidget(pwd_section)
        self.detail_password = QLabel("••••••••••••")
        self.detail_password.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.detail_password.setStyleSheet("font-size: 10pt; font-family: monospace;")
        details_card_layout.addWidget(self.detail_password)
        pwd_btn_layout = QHBoxLayout()
        pwd_btn_layout.setSpacing(8)
        copy_pwd_btn = QPushButton("Copy Password")
        copy_pwd_btn.setObjectName("secondaryBtn")
        copy_pwd_btn.clicked.connect(self.copy_password)
        show_pwd_btn = QPushButton("Show/Hide")
        show_pwd_btn.setObjectName("secondaryBtn")
        show_pwd_btn.clicked.connect(self.toggle_detail_password)
        pwd_btn_layout.addWidget(copy_pwd_btn)
        pwd_btn_layout.addWidget(show_pwd_btn)
        pwd_btn_layout.addStretch()
        details_card_layout.addLayout(pwd_btn_layout)
        
        # URL section
        url_section = QLabel("WEBSITE URL")
        url_section.setObjectName("sectionLabel")
        details_card_layout.addWidget(url_section)
        self.detail_url = QLabel("")
        self.detail_url.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.detail_url.setWordWrap(True)
        self.detail_url.setStyleSheet("font-size: 10pt;")
        details_card_layout.addWidget(self.detail_url)
        copy_url_btn = QPushButton("Copy URL")
        copy_url_btn.setObjectName("secondaryBtn")
        copy_url_btn.setFixedWidth(120)
        copy_url_btn.clicked.connect(self.copy_url)
        details_card_layout.addWidget(copy_url_btn)
        
        # Notes section
        notes_section = QLabel("NOTES")
        notes_section.setObjectName("sectionLabel")
        details_card_layout.addWidget(notes_section)
        self.detail_notes = QTextEdit()
        self.detail_notes.setReadOnly(True)
        self.detail_notes.setMinimumHeight(100)
        details_card_layout.addWidget(self.detail_notes)
        
        details_card_layout.addStretch()
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(8)
        edit_btn = QPushButton("✏️ Edit")
        edit_btn.setObjectName("secondaryBtn")
        edit_btn.clicked.connect(self.edit_entry)
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setObjectName("dangerBtn")
        delete_btn.clicked.connect(self.delete_entry)
        action_layout.addStretch()
        action_layout.addWidget(edit_btn)
        action_layout.addWidget(delete_btn)
        details_card_layout.addLayout(action_layout)
        
        right_layout.addWidget(details_card)
        splitter.addWidget(right_widget)
        
        splitter.setSizes([280, 620])
        container_layout.addWidget(splitter)
        self.main_layout.addWidget(container)
        
        self.refresh_entry_list()
    
    def refresh_entry_list(self, entries=None):
        """Refresh the entry list"""
        self.entry_list.clear()
        if entries is None:
            entries = self.vault.get_entries()
        
        for entry in entries:
            item = QListWidgetItem(entry.get('title', 'Untitled'))
            item.setData(Qt.ItemDataRole.UserRole, entry['id'])
            self.entry_list.addItem(item)
    
    def filter_entries(self, text):
        """Filter entries based on search"""
        if not text:
            self.refresh_entry_list()
        else:
            results = self.vault.search_entries(text)
            self.refresh_entry_list(results)
    
    def show_entry_details(self, item):
        """Show details of selected entry"""
        if item is None:
            return
        entry_id = item.data(Qt.ItemDataRole.UserRole)
        self.current_entry_id = entry_id
        entry = self.vault.get_entry(entry_id)
        
        if entry:
            self.detail_title.setText(entry.get('title', 'Untitled'))
            self.detail_username.setText(entry.get('username', '') or "—")
            self.actual_password = entry.get('password', '')
            self.detail_password.setText("••••••••••••")
            self.password_shown = False
            self.detail_url.setText(entry.get('url', '') or "—")
            self.detail_notes.setPlainText(entry.get('notes', '') or "")
    
    def copy_username(self):
        if self.current_entry_id:
            entry = self.vault.get_entry(self.current_entry_id)
            if entry:
                try:
                    pyperclip.copy(entry.get('username', ''))
                    self.status_label.setText("Username copied to clipboard")
                    QTimer.singleShot(30000, lambda: self.status_label.setText("Unlocked"))
                except Exception as e:
                    self.status_label.setText("Failed to copy to clipboard")
                    QMessageBox.warning(self, "Clipboard Error", 
                        "Could not copy to clipboard. Please install a clipboard manager.\n"
                        "For Wayland: sudo apt install wl-clipboard\n"
                        "For X11: sudo apt install xclip")
    
    def copy_password(self):
        if self.current_entry_id:
            entry = self.vault.get_entry(self.current_entry_id)
            if entry:
                try:
                    pyperclip.copy(entry.get('password', ''))
                    self.status_label.setText("Password copied to clipboard (will clear in 30s)")
                    QTimer.singleShot(30000, lambda: self._safe_clear_clipboard())
                    QTimer.singleShot(30000, lambda: self.status_label.setText("Unlocked"))
                except Exception as e:
                    self.status_label.setText("Failed to copy to clipboard")
                    QMessageBox.warning(self, "Clipboard Error", 
                        "Could not copy to clipboard. Please install a clipboard manager.\n"
                        "For Wayland: sudo apt install wl-clipboard\n"
                        "For X11: sudo apt install xclip")
    
    def _safe_clear_clipboard(self):
        try:
            pyperclip.copy('')
        except:
            pass
    
    def copy_url(self):
        if self.current_entry_id:
            entry = self.vault.get_entry(self.current_entry_id)
            if entry:
                try:
                    pyperclip.copy(entry.get('url', ''))
                    self.status_label.setText("URL copied to clipboard")
                    QTimer.singleShot(30000, lambda: self.status_label.setText("Unlocked"))
                except Exception as e:
                    self.status_label.setText("Failed to copy to clipboard")
                    QMessageBox.warning(self, "Clipboard Error", 
                        "Could not copy to clipboard. Please install a clipboard manager.\n"
                        "For Wayland: sudo apt install wl-clipboard\n"
                        "For X11: sudo apt install xclip")
    
    def toggle_detail_password(self):
        if not hasattr(self, 'password_shown'):
            self.password_shown = False
        if self.password_shown:
            self.detail_password.setText("••••••••••••")
            self.password_shown = False
        else:
            if hasattr(self, 'actual_password'):
                self.detail_password.setText(self.actual_password)
            self.password_shown = True
    
    def add_entry(self):
        dialog = AddEditDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if not data['title']:
                QMessageBox.warning(self, "Error", "Title is required")
                return
            self.vault.add_entry(**data)
            self.vault.save_vault(self.master_password)
            self.refresh_entry_list()
            self.status_label.setText("Entry added")
    
    def edit_entry(self):
        if not self.current_entry_id:
            QMessageBox.warning(self, "Error", "No entry selected")
            return
        entry = self.vault.get_entry(self.current_entry_id)
        dialog = AddEditDialog(self, entry)
        if dialog.exec():
            data = dialog.get_data()
            self.vault.update_entry(self.current_entry_id, **data)
            self.vault.save_vault(self.master_password)
            self.refresh_entry_list()
            current = self.entry_list.currentItem()
            if current:
                self.show_entry_details(current)
            self.status_label.setText("Entry updated")
    
    def delete_entry(self):
        if not self.current_entry_id:
            QMessageBox.warning(self, "Error", "No entry selected")
            return
        reply = QMessageBox.question(self, "Confirm Delete",
            "Are you sure you want to delete this entry?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.vault.delete_entry(self.current_entry_id)
            self.vault.save_vault(self.master_password)
            self.refresh_entry_list()
            self.detail_title.setText("Select an entry")
            self.detail_username.setText("")
            self.detail_password.setText("••••••••")
            self.detail_url.setText("")
            self.detail_notes.clear()
            self.current_entry_id = None
            self.status_label.setText("Entry deleted")
    
    def show_password_generator(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Password Generator")
        dialog.setMinimumWidth(400)
        dialog.setMinimumHeight(420)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        title = QLabel("🎲 Password Generator")
        title.setObjectName("cardTitle")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Length
        length_label = QLabel("Length")
        length_label.setObjectName("sectionLabel")
        layout.addWidget(length_label)
        length_spin = QSpinBox()
        length_spin.setRange(4, 64)
        length_spin.setValue(16)
        length_spin.setMinimumHeight(38)
        layout.addWidget(length_spin)
        
        # Options
        options_label = QLabel("CHARACTER OPTIONS")
        options_label.setObjectName("sectionLabel")
        layout.addWidget(options_label)
        
        lower_check = QCheckBox("Lowercase letters (a-z)")
        lower_check.setChecked(True)
        upper_check = QCheckBox("Uppercase letters (A-Z)")
        upper_check.setChecked(True)
        digit_check = QCheckBox("Numbers (0-9)")
        digit_check.setChecked(True)
        symbol_check = QCheckBox("Symbols (!@#$%^&*)")
        symbol_check.setChecked(True)
        
        layout.addWidget(lower_check)
        layout.addWidget(upper_check)
        layout.addWidget(digit_check)
        layout.addWidget(symbol_check)
        
        # Result
        result_label = QLabel("GENERATED PASSWORD")
        result_label.setObjectName("sectionLabel")
        layout.addWidget(result_label)
        result_input = QLineEdit()
        result_input.setReadOnly(True)
        result_input.setMinimumHeight(40)
        result_input.setStyleSheet("font-family: monospace; font-size: 10pt;")
        layout.addWidget(result_input)
        
        gen_btn = QPushButton("Generate New Password")
        def generate():
            pwd = self.generator.generate(
                length_spin.value(),
                lower_check.isChecked(),
                upper_check.isChecked(),
                digit_check.isChecked(),
                symbol_check.isChecked()
            )
            result_input.setText(pwd)
        gen_btn.clicked.connect(generate)
        layout.addWidget(gen_btn)
        
        copy_btn = QPushButton("Copy to Clipboard")
        copy_btn.setObjectName("secondaryBtn")
        def copy_gen():
            try:
                if result_input.text():
                    pyperclip.copy(result_input.text())
                    self.status_label.setText("Password copied to clipboard")
                    QTimer.singleShot(2000, lambda: self.status_label.setText("🔓 Unlocked" if self.vault.is_unlocked else "🔒 Locked"))
            except:
                QMessageBox.warning(dialog, "Clipboard Error", 
                    "Could not copy to clipboard.\n"
                    "For Wayland: sudo apt install wl-clipboard\n"
                    "For X11: sudo apt install xclip")
        copy_btn.clicked.connect(copy_gen)
        layout.addWidget(copy_btn)
        
        layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.setObjectName("secondaryBtn")
        close_btn.clicked.connect(dialog.reject)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        generate()
        dialog.exec()
    
    def start_inactivity_timer(self):
        self.lock_timer.start(60000)  # Check every minute
    
    def auto_lock(self):
        if self.vault.is_unlocked:
            # Simple auto-lock after timeout of inactivity
            # For demo purposes, just lock after 5 minutes from start
            if time.time() - self.last_activity > self.inactivity_timeout / 1000:
                self.lock_vault()
    
    def lock_vault(self):
        if self.vault.is_unlocked:
            self.vault.lock_vault()
            self.clear_main_area()
            self.show_lock_screen()
            self.lock_timer.stop()
            self.status_label.setText("🔒 Locked")
