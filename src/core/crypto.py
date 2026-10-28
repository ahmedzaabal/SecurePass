"""
Cryptographic operations for SecurePass
Uses Argon2id for key derivation and AES-256-GCM for encryption
"""

import os
import json
import base64
from typing import Tuple, Dict, Any
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2.low_level import hash_secret_raw, Type

class CryptoManager:
    """Handles all cryptographic operations"""
    
    # Argon2id parameters - secure defaults
    ARGON2_TIME_COST = 3
    ARGON2_MEMORY_COST = 65536  # 64 MB
    ARGON2_PARALLELISM = 4
    ARGON2_HASH_LEN = 32  # 256 bits for AES-256
    SALT_LEN = 32
    
    def __init__(self):
        pass
    
    def generate_salt(self) -> bytes:
        """Generate a cryptographically secure random salt"""
        return os.urandom(self.SALT_LEN)
    
    def derive_key(self, master_password: str, salt: bytes) -> bytes:
        """
        Derive encryption key from master password using Argon2id
        """
        if isinstance(master_password, str):
            password_bytes = master_password.encode('utf-8')
        else:
            password_bytes = master_password
        
        key = hash_secret_raw(
            secret=password_bytes,
            salt=salt,
            time_cost=self.ARGON2_TIME_COST,
            memory_cost=self.ARGON2_MEMORY_COST,
            parallelism=self.ARGON2_PARALLELISM,
            hash_len=self.ARGON2_HASH_LEN,
            type=Type.ID
        )
        return key
    
    def encrypt(self, plaintext: str, key: bytes) -> Tuple[bytes, bytes]:
        """
        Encrypt plaintext using AES-256-GCM
        Returns (ciphertext, nonce)
        """
        if isinstance(plaintext, str):
            plaintext_bytes = plaintext.encode('utf-8')
        else:
            plaintext_bytes = plaintext
        
        nonce = os.urandom(12)  # 96-bit nonce for GCM
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, plaintext_bytes, None)
        return ciphertext, nonce
    
    def decrypt(self, ciphertext: bytes, nonce: bytes, key: bytes) -> str:
        """
        Decrypt ciphertext using AES-256-GCM
        Returns plaintext string
        """
        aesgcm = AESGCM(key)
        plaintext_bytes = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext_bytes.decode('utf-8')
    
    def encrypt_vault(self, vault_data: Dict[str, Any], master_password: str) -> Dict[str, str]:
        """
        Encrypt the entire vault data structure
        Returns a dictionary with base64-encoded encrypted data
        """
        salt = self.generate_salt()
        key = self.derive_key(master_password, salt)
        
        # Serialize vault data
        plaintext = json.dumps(vault_data, ensure_ascii=False)
        
        # Encrypt
        ciphertext, nonce = self.encrypt(plaintext, key)
        
        # Return as base64-encoded strings for storage
        return {
            'version': '1.0',
            'salt': base64.b64encode(salt).decode('utf-8'),
            'nonce': base64.b64encode(nonce).decode('utf-8'),
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'algorithm': 'AES-256-GCM',
            'kdf': 'Argon2id'
        }
    
    def decrypt_vault(self, encrypted_vault: Dict[str, str], master_password: str) -> Dict[str, Any]:
        """
        Decrypt the entire vault data structure
        """
        salt = base64.b64decode(encrypted_vault['salt'])
        nonce = base64.b64decode(encrypted_vault['nonce'])
        ciphertext = base64.b64decode(encrypted_vault['ciphertext'])
        
        key = self.derive_key(master_password, salt)
        plaintext = self.decrypt(ciphertext, nonce, key)
        
        return json.loads(plaintext)
