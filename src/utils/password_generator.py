"""
Password generator utility
"""

import random
import string
import secrets

class PasswordGenerator:
    """Generate secure random passwords"""
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = '!@#$%^&*()_+-=[]{}|;:,.<>?'
    
    def generate(self, length: int = 16, 
                 use_lowercase: bool = True,
                 use_uppercase: bool = True,
                 use_digits: bool = True,
                 use_symbols: bool = True) -> str:
        """
        Generate a random password
        """
        if length < 4:
            length = 4
        
        charset = ''
        required = []
        
        if use_lowercase:
            charset += self.lowercase
            required.append(secrets.choice(self.lowercase))
        
        if use_uppercase:
            charset += self.uppercase
            required.append(secrets.choice(self.uppercase))
        
        if use_digits:
            charset += self.digits
            required.append(secrets.choice(self.digits))
        
        if use_symbols:
            charset += self.symbols
            required.append(secrets.choice(self.symbols))
        
        if not charset:
            charset = self.lowercase + self.digits
        
        # Generate remaining characters
        password = list(required)
        for _ in range(length - len(required)):
            password.append(secrets.choice(charset))
        
        # Shuffle to avoid predictable positions
        random.shuffle(password)
        
        return ''.join(password)
    
    def calculate_strength(self, password: str) -> tuple:
        """
        Calculate password strength
        Returns (score, description) where score is 0-5
        """
        score = 0
        
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        if any(c.islower() for c in password):
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in self.symbols for c in password):
            score += 1
        
        # Normalize to 0-5
        score = min(5, score // 1)
        if len(password) >= 16 and any(c.islower() for c in password) and \
           any(c.isupper() for c in password) and any(c.isdigit() for c in password) and \
           any(c in self.symbols for c in password):
            score = 5
        
        descriptions = ["Very Weak", "Weak", "Fair", "Good", "Strong", "Very Strong"]
        return score, descriptions[score]
