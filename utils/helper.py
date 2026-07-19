"""
DPassGen Helper Utilities
Helper functions and utilities
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manage application configuration"""
    
    DEFAULT_CONFIG = {
        "default_length": 16,
        "default_options": {
            "uppercase": True,
            "lowercase": True,
            "numbers": True,
            "symbols": True
        },
        "theme": "cyberpunk",
        "animation": True,
        "auto_copy": False,
        "exclude_similar": False,
        "exclude_ambiguous": False
    }
    
    def __init__(self, config_path: Optional[str] = None):
        if config_path:
            self.config_path = Path(config_path).expanduser()
        else:
            self.config_path = Path(__file__).parent.parent / "config.json"
        
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self.DEFAULT_CONFIG.copy()
        else:
            return self.DEFAULT_CONFIG.copy()
    
    def _save_config(self) -> None:
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self._config, f, indent=4)
        except IOError as e:
            print(f"Warning: Could not save config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self._config[key] = value
        self._save_config()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration"""
        return self._config.copy()
    
    def reset(self) -> None:
        """Reset to default configuration"""
        self._config = self.DEFAULT_CONFIG.copy()
        self._save_config()


class ColorFormatter:
    """Format text with colors for terminal"""
    
    # ANSI color codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    @classmethod
    def colorize(cls, text: str, fg: str = WHITE, bg: str = None, bold: bool = False) -> str:
        """Colorize text with foreground and optional background"""
        result = ""
        
        if bold:
            result += cls.BOLD
        
        result += fg + text + cls.RESET
        
        if bg:
            result = bg + result + cls.RESET
        
        return result
    
    @classmethod
    def cyan(cls, text: str, bold: bool = False) -> str:
        """Cyan text"""
        return cls.colorize(text, cls.CYAN, bold=bold)
    
    @classmethod
    def magenta(cls, text: str, bold: bool = False) -> str:
        """Magenta text"""
        return cls.colorize(text, cls.MAGENTA, bold=bold)
    
    @classmethod
    def green(cls, text: str, bold: bool = False) -> str:
        """Green text"""
        return cls.colorize(text, cls.GREEN, bold=bold)
    
    @classmethod
    def red(cls, text: str, bold: bool = False) -> str:
        """Red text"""
        return cls.colorize(text, cls.RED, bold=bold)
    
    @classmethod
    def yellow(cls, text: str, bold: bool = False) -> str:
        """Yellow text"""
        return cls.colorize(text, cls.YELLOW, bold=bold)
    
    @classmethod
    def white(cls, text: str, bold: bool = False) -> str:
        """White text"""
        return cls.colorize(text, cls.WHITE, bold=bold)
    
    @classmethod
    def clear_line(cls) -> str:
        """Clear current line"""
        return "\r\033[K"
    
    @classmethod
    def move_up(cls, lines: int = 1) -> str:
        """Move cursor up"""
        return f"\033[{lines}A"
    
    @classmethod
    def move_down(cls, lines: int = 1) -> str:
        """Move cursor down"""
        return f"\033[{lines}B"
    
    @classmethod
    def hide_cursor(cls) -> str:
        """Hide cursor"""
        return "\033[?25l"
    
    @classmethod
    def show_cursor(cls) -> str:
        """Show cursor"""
        return "\033[?25h"


def clear_screen() -> None:
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_terminal_size() -> tuple:
    """Get terminal size (columns, rows)"""
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except OSError:
        return 80, 24


def is_termux() -> bool:
    """Check if running in Termux"""
    return os.environ.get('TERMUX', '') == '1' or \
           os.path.exists('/data/data/com.termux')


def supports_color() -> bool:
    """Check if terminal supports colors"""
    if os.environ.get('TERM', '') == 'dumb':
        return False
    
    if not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
        return False
    
    # Check for common color-supporting terminals
    term = os.environ.get('TERM', '')
    color_terms = {'xterm', 'linux', 'screen', 'vt100', 'rxvt', 'ansi'}
    
    return any(t in term.lower() for t in color_terms)


def format_bytes(size: int) -> str:
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate string to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
