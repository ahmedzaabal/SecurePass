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
        self.setWindowTitle("SecurePass - Unlock")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("SecurePass")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        if self.vault_exists:
            subtitle = QLabel("Enter your master password to unlock")
        else:
            subtitle = QLabel("Create your master password")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #666;")
        layout.addWidget(subtitle)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Master Password")
        self.password_input.setMinimumHeight(35)
        self.password_input.returnPressed.connect(self.handle_submit)
        layout.addWidget(self.password_input)
        
        # Confirm password (only for new vault)
        if not self.vault_exists:
            self.confirm_input = QLineEdit()
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirm_input.setPlaceholderText("Confirm Master Password")
            self.confirm_input.setMinimumHeight(35)
            self.confirm_input.returnPressed.connect(self.handle_submit)
            layout.addWidget(self.confirm_input)
            warning = QLabel("⚠️ If you forget this password, your data cannot be recovered!")
            warning.setWordWrap(True)
            warning.setStyleSheet("color: #d33; font-size: 9pt;")
            warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(warning)
        else:
            layout.addSpacing(30)
        
        # Submit button
        if self.vault_exists:
            self.submit_btn = QPushButton("Unlock")
        else:
            self.submit_btn = QPushButton("Create Vault")
        self.submit_btn.setMinimumHeight(35)
        self.submit_btn.clicked.connect(self.handle_submit)
        self.submit_btn.setDefault(True)
        layout.addWidget(self.submit_btn)
        
        layout.addStretch()
        self.setLayout(layout)
    
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
