"""
Lock screen - for creating or unlocking vault
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, 
                             QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class LockScreen(QWidget):
    """Screen for unlocking existing vault or creating new one"""
    
    unlocked = pyqtSignal(str)  # Signal emitted with master password when unlocked
    
    def __init__(self, vault_exists=False):
        super().__init__()
        self.vault_exists = vault_exists
        self.init_ui()
    
    def init_ui(self):
        self.setMinimumSize(450, 380)
        self.setAutoFillBackground(True)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(60, 60, 60, 60)
        main_layout.addStretch()
        
        # Card
        card = QFrame()
        card.setObjectName("card")
        card.setMaximumWidth(380)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(16)
        
        # Title
        title = QLabel("🔐 SecurePass")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)
        
        # Subtitle
        if self.vault_exists:
            subtitle = QLabel("Enter your master password to unlock your vault")
        else:
            subtitle = QLabel("Create a master password to secure your vault")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #a1a1aa;")
        card_layout.addWidget(subtitle)
        
        card_layout.addSpacing(10)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Master Password")
        self.password_input.setMinimumHeight(42)
        self.password_input.returnPressed.connect(self.handle_submit)
        card_layout.addWidget(self.password_input)
        
        # Confirm password (only for new vault)
        if not self.vault_exists:
            self.confirm_input = QLineEdit()
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirm_input.setPlaceholderText("Confirm Master Password")
            self.confirm_input.setMinimumHeight(42)
            self.confirm_input.returnPressed.connect(self.handle_submit)
            card_layout.addWidget(self.confirm_input)
            warning = QLabel("⚠️ If you forget your master password, your data cannot be recovered.")
            warning.setWordWrap(True)
            warning.setStyleSheet("color: #f59e0b; font-size: 8pt;")
            warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(warning)
        
        card_layout.addSpacing(10)
        
        # Submit button
        if self.vault_exists:
            self.submit_btn = QPushButton("Unlock Vault")
        else:
            self.submit_btn = QPushButton("Create Vault")
        self.submit_btn.setMinimumHeight(42)
        self.submit_btn.clicked.connect(self.handle_submit)
        self.submit_btn.setDefault(True)
        card_layout.addWidget(self.submit_btn)
        
        # Center card
        card_container = QHBoxLayout()
        card_container.addStretch()
        card_container.addWidget(card)
        card_container.addStretch()
        main_layout.addLayout(card_container)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def handle_submit(self):
        password = self.password_input.text()
        
        if not password:
            QMessageBox.warning(self, "Error", "Please enter a master password")
            return
        
        if not self.vault_exists:
            confirm = self.confirm_input.text()
            if password != confirm:
                QMessageBox.warning(self, "Error", "Passwords do not match")
                return
            if len(password) < 8:
                reply = QMessageBox.question(self, "Weak Password",
                    "Your password is less than 8 characters. Continue anyway?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.No:
                    return
        
        self.unlocked.emit(password)
