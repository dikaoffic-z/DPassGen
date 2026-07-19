"""
DPassGen Password Analyzer
Analyzes password strength and security
"""

import math
import re
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class PasswordAnalysis:
    """Password analysis result"""
    score: int  # 0-100
    entropy: float  # bits
    strength_label: str
    strength_emoji: str
    crack_time: str
    character_breakdown: Dict[str, int]
    issues: List[str]
    recommendations: List[str]


class PasswordAnalyzer:
    """Analyze password strength and security"""
    
    # Common weak passwords to check
    COMMON_PASSWORDS = {
        "password", "123456", "12345678", "qwerty", "abc123",
        "monkey", "1234567", "letmein", "trustno1", "dragon",
        "baseball", "iloveyou", "master", "sunshine", "ashley",
        "bailey", "passw0rd", "shadow", "123123", "654321",
        "superman", "qazwsx", "michael", "football", "password1",
        "password123", "welcome", "admin", "login", "hello"
    }
    
    # Sequential patterns to detect
    SEQUENTIAL_PATTERNS = [
        "012", "123", "234", "345", "456", "567", "678", "789",
        "987", "876", "765", "654", "543", "432", "321", "210",
        "abc", "bcd", "cde", "def", "efg", "fgh", "ghi", "hij",
        "ijk", "jkl", "klm", "lmn", "mno", "nop", "opq", "pqr",
        "qrs", "rst", "stu", "tuv", "uvw", "vwx", "wxy", "xyz"
    ]
    
    def __init__(self):
        pass
    
    def analyze(self, password: str) -> PasswordAnalysis:
        """Analyze password and return detailed analysis"""
        breakdown = self._get_character_breakdown(password)
        entropy = self._calculate_entropy(password, breakdown)
        score = self._calculate_score(password, entropy, breakdown)
        strength_label, strength_emoji = self._get_strength_label(score)
        crack_time = self._estimate_crack_time(entropy)
        issues = self._find_issues(password, breakdown)
        recommendations = self._get_recommendations(password, breakdown, entropy)
        
        return PasswordAnalysis(
            score=score,
            entropy=entropy,
            strength_label=strength_label,
            strength_emoji=strength_emoji,
            crack_time=crack_time,
            character_breakdown=breakdown,
            issues=issues,
            recommendations=recommendations
        )
    
    def _get_character_breakdown(self, password: str) -> Dict[str, int]:
        """Get count of each character type"""
        breakdown = {
            "uppercase": 0,
            "lowercase": 0,
            "numbers": 0,
            "symbols": 0,
            "other": 0
        }
        
        for char in password:
            if char.isupper():
                breakdown["uppercase"] += 1
            elif char.islower():
                breakdown["lowercase"] += 1
            elif char.isdigit():
                breakdown["numbers"] += 1
            elif char.isascii():
                breakdown["symbols"] += 1
            else:
                breakdown["other"] += 1
        
        return breakdown
    
    def _calculate_entropy(self, password: str, breakdown: Dict[str, int]) -> float:
        """Calculate password entropy in bits"""
        if not password:
            return 0.0
        
        # Count unique character pool
        pool_size = 0
        if breakdown["uppercase"] > 0:
            pool_size += 26
        if breakdown["lowercase"] > 0:
            pool_size += 26
        if breakdown["numbers"] > 0:
            pool_size += 10
        if breakdown["symbols"] > 0:
            pool_size += 32
        if breakdown["other"] > 0:
            pool_size += 128
        
        if pool_size == 0:
            return 0.0
        
        # Entropy = length * log2(pool_size)
        entropy = len(password) * math.log2(pool_size)
        return round(entropy, 2)
    
    def _calculate_score(self, password: str, entropy: float, breakdown: Dict[str, int]) -> int:
        """Calculate password strength score (0-100)"""
        score = 0
        
        # Length score (up to 30 points)
        length = len(password)
        if length >= 16:
            score += 30
        elif length >= 12:
            score += 25
        elif length >= 8:
            score += 15
        elif length >= 6:
            score += 10
        else:
            score += 5
        
        # Character variety score (up to 30 points)
        variety_score = 0
        if breakdown["uppercase"] > 0:
            variety_score += 7.5
        if breakdown["lowercase"] > 0:
            variety_score += 7.5
        if breakdown["numbers"] > 0:
            variety_score += 7.5
        if breakdown["symbols"] > 0:
            variety_score += 7.5
        score += variety_score
        
        # Entropy score (up to 25 points)
        if entropy >= 80:
            score += 25
        elif entropy >= 60:
            score += 20
        elif entropy >= 40:
            score += 15
        elif entropy >= 28:
            score += 10
        else:
            score += 5
        
        # Penalty for common patterns
        password_lower = password.lower()
        if password_lower in self.COMMON_PASSWORDS:
            score = min(score, 10)
        
        # Penalty for sequential patterns
        for pattern in self.SEQUENTIAL_PATTERNS:
            if pattern in password_lower:
                score = max(0, score - 5)
                break
        
        # Penalty for repeated characters
        if len(set(password)) < len(password) / 2:
            score = max(0, score - 10)
        
        # Penalty for predictable structures
        if re.match(r'^[a-z]+\d+$', password_lower):
            score = max(0, score - 15)
        if password.isdigit():
            score = max(0, score - 20)
        
        return min(100, max(0, int(score)))
    
    def _get_strength_label(self, score: int) -> tuple:
        """Get strength label and emoji based on score"""
        if score >= 80:
            return "Very Strong", "🔵"
        elif score >= 60:
            return "Strong", "🟢"
        elif score >= 40:
            return "Medium", "🟡"
        elif score >= 20:
            return "Weak", "🟠"
        else:
            return "Very Weak", "🔴"
    
    def _estimate_crack_time(self, entropy: float) -> str:
        """Estimate time to crack password"""
        # Assuming 10 billion guesses per second (modern GPU cluster)
        guesses_per_second = 10_000_000_000
        possible_combinations = 2 ** entropy
        seconds = possible_combinations / guesses_per_second / 2  # Average case
        
        if seconds < 1:
            return "Instant"
        elif seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            return f"{int(seconds / 60)} minutes"
        elif seconds < 86400:
            return f"{int(seconds / 3600)} hours"
        elif seconds < 31536000:
            return f"{int(seconds / 86400)} days"
        elif seconds < 31536000 * 100:
            return f"{int(seconds / 31536000)} years"
        elif seconds < 31536000 * 1000000:
            years = int(seconds / 31536000)
            return f"{years:,} years"
        elif seconds < 31536000 * 1000000000:
            years = int(seconds / 31536000)
            return f"{years:,} years"
        else:
            return "Centuries+"
    
    def _find_issues(self, password: str, breakdown: Dict[str, int]) -> List[str]:
        """Find security issues in password"""
        issues = []
        password_lower = password.lower()
        
        # Check for common passwords
        if password_lower in self.COMMON_PASSWORDS:
            issues.append("Password is in the list of most common passwords")
        
        # Check length
        if len(password) < 8:
            issues.append("Password is too short (less than 8 characters)")
        
        # Check for only one character type
        active_types = sum(1 for v in [breakdown["uppercase"], breakdown["lowercase"],
                                        breakdown["numbers"], breakdown["symbols"]] if v > 0)
        if active_types == 1:
            issues.append("Password uses only one character type")
        elif active_types == 2:
            issues.append("Password uses only two character types")
        
        # Check for sequential patterns
        for pattern in self.SEQUENTIAL_PATTERNS:
            if pattern in password_lower:
                issues.append(f"Contains sequential pattern: {pattern}")
                break
        
        # Check for repeated characters
        if len(set(password)) < len(password) / 3:
            issues.append("Contains too many repeated characters")
        
        # Check for keyboard patterns
        keyboard_patterns = ["qwerty", "asdf", "zxcv", "qazwsx"]
        for pattern in keyboard_patterns:
            if pattern in password_lower:
                issues.append(f"Contains keyboard pattern: {pattern}")
                break
        
        # Check for only numbers
        if breakdown["numbers"] == len(password):
            issues.append("Password contains only numbers")
        
        # Check for year patterns
        if re.search(r'19\d{2}|20\d{2}', password):
            issues.append("Contains year pattern (often used in passwords)")
        
        return issues
    
    def _get_recommendations(self, password: str, breakdown: Dict[str, int], entropy: float) -> List[str]:
        """Get security recommendations"""
        recommendations = []
        
        # Length recommendation
        if len(password) < 12:
            recommendations.append("Use at least 12 characters for better security")
        elif len(password) < 16:
            recommendations.append("Consider using 16+ characters for maximum security")
        
        # Character variety
        if breakdown["uppercase"] == 0:
            recommendations.append("Add uppercase letters (A-Z)")
        if breakdown["lowercase"] == 0:
            recommendations.append("Add lowercase letters (a-z)")
        if breakdown["numbers"] == 0:
            recommendations.append("Add numbers (0-9)")
        if breakdown["symbols"] == 0:
            recommendations.append("Add special characters (!@#$%^&*)")
        
        # Entropy
        if entropy < 40:
            recommendations.append("Increase password complexity to raise entropy above 40 bits")
        
        # General recommendations
        if len(recommendations) == 0:
            recommendations.append("Password meets basic security requirements")
            if entropy < 60:
                recommendations.append("Consider using a longer or more complex password")
        
        return recommendations
