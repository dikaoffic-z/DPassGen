"""
DPassGen Security Module
Secure password generation using secrets module
"""

import secrets
import hashlib
import os
from typing import List


class SecurityEngine:
    """Security engine for cryptographically secure operations"""
    
    UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
    NUMBERS = "0123456789"
    SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    SIMILAR_CHARS = "iIlL1oO0"
    AMBIGUOUS_CHARS = "{}[]()/\\'\"`~,;:.<>"
    
    @staticmethod
    def secure_choice(characters: str) -> str:
        """Securely choose a random character from string"""
        return secrets.choice(characters)
    
    @staticmethod
    def secure_token_bytes(n: int) -> bytes:
        """Generate cryptographically secure random bytes"""
        return secrets.token_bytes(n)
    
    @staticmethod
    def secure_random_int(a: int, b: int) -> int:
        """Generate secure random integer in range [a, b]"""
        return secrets.randbelow(b - a + 1) + a
    
    @classmethod
    def shuffle_secure(cls, sequence: List[str]) -> List[str]:
        """Securely shuffle a list using Fisher-Yates with secrets"""
        result = sequence.copy()
        for i in range(len(result) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            result[i], result[j] = result[j], result[i]
        return result
    
    @classmethod
    def get_character_pool(
        cls,
        uppercase: bool = True,
        lowercase: bool = True,
        numbers: bool = True,
        symbols: bool = True,
        custom_chars: str = "",
        exclude_similar: bool = False,
        exclude_ambiguous: bool = False
    ) -> str:
        """Build character pool based on options"""
        pool = ""
        
        if uppercase:
            chars = cls.UPPERCASE
            if exclude_similar:
                chars = cls._remove_similar(chars)
            if exclude_ambiguous:
                chars = cls._remove_ambiguous(chars)
            pool += chars
        
        if lowercase:
            chars = cls.LOWERCASE
            if exclude_similar:
                chars = cls._remove_similar(chars)
            if exclude_ambiguous:
                chars = cls._remove_ambiguous(chars)
            pool += chars
        
        if numbers:
            chars = cls.NUMBERS
            if exclude_similar:
                chars = cls._remove_similar(chars)
            if exclude_ambiguous:
                chars = cls._remove_ambiguous(chars)
            pool += chars
        
        if symbols:
            pool += cls.SYMBOLS
        
        pool += custom_chars
        
        return pool
    
    @staticmethod
    def _remove_similar(chars: str) -> str:
        """Remove similar characters that can be confused"""
        return "".join(c for c in chars if c not in SecurityEngine.SIMILAR_CHARS)
    
    @staticmethod
    def _remove_ambiguous(chars: str) -> str:
        """Remove ambiguous characters"""
        return "".join(c for c in chars if c not in SecurityEngine.AMBIGUOUS_CHARS)
    
    @staticmethod
    def calculate_entropy(length: int, pool_size: int) -> float:
        """Calculate password entropy in bits"""
        if pool_size <= 0 or length <= 0:
            return 0.0
        return length * (hashlib.log2(pool_size))
    
    @staticmethod
    def hash_md5(text: str) -> str:
        """Generate MD5 hash"""
        return hashlib.md5(text.encode()).hexdigest()
    
    @staticmethod
    def hash_sha1(text: str) -> str:
        """Generate SHA1 hash"""
        return hashlib.sha1(text.encode()).hexdigest()
    
    @staticmethod
    def hash_sha256(text: str) -> str:
        """Generate SHA256 hash"""
        return hashlib.sha256(text.encode()).hexdigest()
    
    @staticmethod
    def hash_sha384(text: str) -> str:
        """Generate SHA384 hash"""
        return hashlib.sha384(text.encode()).hexdigest()
    
    @staticmethod
    def hash_sha512(text: str) -> str:
        """Generate SHA512 hash"""
        return hashlib.sha512(text.encode()).hexdigest()
