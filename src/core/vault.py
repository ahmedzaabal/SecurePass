"""
Vault management for SecurePass
Handles loading, saving, and managing password entries
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from core.crypto import CryptoManager

class Vault:
    """Manages the password vault"""
    
    def __init__(self):
        self.crypto = CryptoManager()
        self.vault_path = self._get_vault_path()
        self.data = None
        self.encryption_key = None
        self.is_unlocked = False
    
    def _get_vault_path(self) -> Path:
        """Get the default vault file path"""
        if os.name == 'nt':  # Windows
            base_dir = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
        elif os.name == 'posix':
            if os.uname().sysname == 'Darwin':  # macOS
                base_dir = Path.home() / 'Library' / 'Application Support'
            else:  # Linux
                base_dir = Path.home() / '.local' / 'share'
        else:
            base_dir = Path.home()
        
        vault_dir = base_dir / 'SecurePass'
        vault_dir.mkdir(parents=True, exist_ok=True)
        return vault_dir / 'vault.secure'
    
    def vault_exists(self) -> bool:
        """Check if a vault file exists"""
        return self.vault_path.exists()
    
    def create_vault(self, master_password: str) -> bool:
        """Create a new vault with master password"""
        try:
            initial_data = {
                'version': '1.0',
                'created_at': datetime.now().isoformat(),
                'entries': []
            }
            
            encrypted = self.crypto.encrypt_vault(initial_data, master_password)
            
            with open(self.vault_path, 'w', encoding='utf-8') as f:
                json.dump(encrypted, f, indent=2)
            
            self.data = initial_data
            self.encryption_key = self.crypto.derive_key(
                master_password, 
                __import__('base64').b64decode(encrypted['salt'])
            )
            self.is_unlocked = True
            return True
        except Exception as e:
            print(f"Error creating vault: {e}")
            return False
    
    def unlock_vault(self, master_password: str) -> bool:
        """Unlock an existing vault"""
        try:
            if not self.vault_exists():
                return False
            
            with open(self.vault_path, 'r', encoding='utf-8') as f:
                encrypted = json.load(f)
            
            self.data = self.crypto.decrypt_vault(encrypted, master_password)
            self.encryption_key = self.crypto.derive_key(
                master_password,
                __import__('base64').b64decode(encrypted['salt'])
            )
            self.is_unlocked = True
            return True
        except Exception as e:
            print(f"Error unlocking vault: {e}")
            return False
    
    def lock_vault(self):
        """Lock the vault"""
        self.data = None
        self.encryption_key = None
        self.is_unlocked = False
    
    def save_vault(self, master_password: str) -> bool:
        """Save vault data to disk"""
        try:
            if not self.is_unlocked or self.data is None:
                return False
            
            encrypted = self.crypto.encrypt_vault(self.data, master_password)
            with open(self.vault_path, 'w', encoding='utf-8') as f:
                json.dump(encrypted, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving vault: {e}")
            return False
    
    def add_entry(self, title: str, username: str, password: str, 
                  url: str = "", notes: str = "") -> str:
        """Add a new password entry"""
        if not self.is_unlocked or self.data is None:
            raise Exception("Vault is locked")
        
        entry_id = str(uuid.uuid4())
        entry = {
            'id': entry_id,
            'title': title,
            'username': username,
            'password': password,
            'url': url,
            'notes': notes,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        self.data['entries'].append(entry)
        return entry_id
    
    def update_entry(self, entry_id: str, **kwargs) -> bool:
        """Update an existing entry"""
        if not self.is_unlocked or self.data is None:
            return False
        
        for entry in self.data['entries']:
            if entry['id'] == entry_id:
                entry.update(kwargs)
                entry['updated_at'] = datetime.now().isoformat()
                return True
        return False
    
    def delete_entry(self, entry_id: str) -> bool:
        """Delete an entry"""
        if not self.is_unlocked or self.data is None:
            return False
        
        initial_count = len(self.data['entries'])
        self.data['entries'] = [e for e in self.data['entries'] if e['id'] != entry_id]
        return len(self.data['entries']) < initial_count
    
    def get_entries(self) -> List[Dict[str, Any]]:
        """Get all entries"""
        if not self.is_unlocked or self.data is None:
            return []
        return self.data['entries']
    
    def get_entry(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific entry"""
        for entry in self.get_entries():
            if entry['id'] == entry_id:
                return entry
        return None
    
    def search_entries(self, query: str) -> List[Dict[str, Any]]:
        """Search entries by title, username, or URL"""
        query_lower = query.lower()
        results = []
        for entry in self.get_entries():
            if (query_lower in entry.get('title', '').lower() or
                query_lower in entry.get('username', '').lower() or
                query_lower in entry.get('url', '').lower()):
                results.append(entry)
        return results
