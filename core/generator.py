"""
DPassGen Password Generator Module
Generate secure passwords using cryptographic methods
"""

import secrets
from typing import List, Optional
from .security import SecurityEngine


class PasswordGenerator:
    """Secure password generator using secrets module"""
    
    def __init__(self):
        self.security = SecurityEngine()
    
    def generate(
        self,
        length: int = 16,
        uppercase: bool = True,
        lowercase: bool = True,
        numbers: bool = True,
        symbols: bool = True,
        custom_chars: str = "",
        exclude_similar: bool = False,
        exclude_ambiguous: bool = False,
        force_include: List[str] = None
    ) -> str:
        """
        Generate a secure password with specified options
        
        Args:
            length: Password length (4-2048)
            uppercase: Include uppercase letters
            lowercase: Include lowercase letters
            numbers: Include numbers
            symbols: Include symbols
            custom_chars: Custom characters to include
            exclude_similar: Exclude similar characters (i, l, 1, etc.)
            exclude_ambiguous: Exclude ambiguous characters
            force_include: Force include specific characters
        
        Returns:
            Generated secure password
        """
        # Validate length
        length = max(4, min(2048, length))
        
        # Build character pool
        pool = self.security.get_character_pool(
            uppercase=uppercase,
            lowercase=lowercase,
            numbers=numbers,
            symbols=symbols,
            custom_chars=custom_chars,
            exclude_similar=exclude_similar,
            exclude_ambiguous=exclude_ambiguous
        )
        
        if not pool:
            raise ValueError("Character pool is empty. Enable at least one character type.")
        
        # Generate password
        password = []
        
        # Force include required characters
        if force_include:
            for char in force_include:
                if char in pool:
                    password.append(char)
        
        # Fill remaining length with random characters
        remaining_length = length - len(password)
        for _ in range(remaining_length):
            password.append(self.security.secure_choice(pool))
        
        # Secure shuffle
        password = self.security.shuffle_secure(password)
        
        return "".join(password)
    
    def generate_bulk(
        self,
        count: int,
        length: int = 16,
        uppercase: bool = True,
        lowercase: bool = True,
        numbers: bool = True,
        symbols: bool = True,
        custom_chars: str = "",
        exclude_similar: bool = False,
        exclude_ambiguous: bool = False,
        prefix: str = ""
    ) -> List[str]:
        """
        Generate multiple passwords at once
        
        Args:
            count: Number of passwords to generate
            length: Length of each password
            prefix: Optional prefix for each password
        
        Returns:
            List of generated passwords
        """
        passwords = []
        for i in range(count):
            pwd = self.generate(
                length=length,
                uppercase=uppercase,
                lowercase=lowercase,
                numbers=numbers,
                symbols=symbols,
                custom_chars=custom_chars,
                exclude_similar=exclude_similar,
                exclude_ambiguous=exclude_ambiguous
            )
            if prefix:
                pwd = f"{prefix}{pwd}"
            passwords.append(pwd)
        
        return passwords
    
    def generate_passphrase(
        self,
        word_count: int = 4,
        separator: str = "-",
        add_number: bool = True,
        capitalize: bool = True,
        words: Optional[List[str]] = None
    ) -> str:
        """
        Generate a memorable passphrase
        
        Args:
            word_count: Number of words in passphrase
            separator: Separator between words
            add_number: Add random number at the end
            capitalize: Capitalize first letter of each word
            words: Custom word list (uses default if None)
        
        Returns:
            Generated passphrase
        """
        if words is None:
            words = self._default_words
        
        passphrase_words = []
        for _ in range(word_count):
            word = secrets.choice(words)
            if capitalize:
                word = word.capitalize()
            passphrase_words.append(word)
        
        passphrase = separator.join(passphrase_words)
        
        if add_number:
            number = secrets.randbelow(100)
            passphrase += separator + str(number)
        
        return passphrase
    
    @property
    def _default_words(self) -> List[str]:
        """Default word list for passphrase generation"""
        return [
            "mountain", "river", "ocean", "forest", "desert", "valley", "canyon",
            "island", "coast", "glacier", "volcano", "meadow", "prairie", "jungle",
            "sunrise", "sunset", "thunder", "lightning", "rainbow", "aurora",
            "crystal", "diamond", "emerald", "ruby", "sapphire", "pearl", "amber",
            "phoenix", "dragon", "falcon", "eagle", "panther", "tiger", "wolf",
            "coffee", "cinnamon", "vanilla", "honey", "maple", "ginger", "pepper",
            "harbor", "bridge", "castle", "tower", "temple", "palace", "village",
            "mystery", "wonder", "magic", "legend", "quest", "journey", "adventure",
            "silver", "golden", "bronze", "copper", "iron", "steel", "titanium",
            "quantum", "cosmic", "stellar", "nebula", "galaxy", "comet", "meteor",
            "harmony", "melody", "rhythm", "symphony", "harmony", "sonata", "chorus",
            "velocity", "momentum", "energy", "plasma", "photon", "proton", "neutron"
        ]
