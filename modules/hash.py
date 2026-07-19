"""
DPassGen Hash Module
Hash generation functionality
"""

import pyperclip
from typing import Dict
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.box import ROUNDED
from rich.text import Text

from core.security import SecurityEngine
from ui.theme import CyberpunkTheme


class HashModule:
    """Hash generation module"""
    
    SUPPORTED_HASHES = {
        "MD5": "md5",
        "SHA1": "sha1",
        "SHA256": "sha256",
        "SHA384": "sha384",
        "SHA512": "sha512"
    }
    
    def __init__(self, console: Console, theme: CyberpunkTheme, config: dict):
        self.console = console
        self.theme = theme
        self.config = config
        self.security = SecurityEngine()
    
    def generate_hash(self, text: str, hash_type: str = "sha256") -> str:
        """Generate hash of text"""
        hash_funcs = {
            "md5": self.security.hash_md5,
            "sha1": self.security.hash_sha1,
            "sha256": self.security.hash_sha256,
            "sha384": self.security.hash_sha384,
            "sha512": self.security.hash_sha512
        }
        
        if hash_type.lower() not in hash_funcs:
            raise ValueError(f"Unsupported hash type: {hash_type}")
        
        result = hash_funcs[hash_type.lower()](text)
        
        # Display result
        self._display_hash_result(text, hash_type.upper(), result)
        
        # Copy to clipboard if enabled
        if self.config.get("auto_copy", False):
            try:
                pyperclip.copy(result)
                self.console.print(
                    self.theme.success("✓ Hash copied to clipboard!")
                )
            except:
                pass
        
        return result
    
    def generate_all_hashes(self, text: str) -> Dict[str, str]:
        """Generate all supported hashes"""
        results = {}
        
        for name, key in self.SUPPORTED_HASHES.items():
            hash_funcs = {
                "md5": self.security.hash_md5,
                "sha1": self.security.hash_sha1,
                "sha256": self.security.hash_sha256,
                "sha384": self.security.hash_sha384,
                "sha512": self.security.hash_sha512
            }
            results[name] = hash_funcs[key](text)
        
        # Display results
        self._display_all_hashes(text, results)
        
        return results
    
    def _display_hash_result(self, text: str, hash_type: str, result: str) -> None:
        """Display single hash result"""
        self.console.print()
        
        # Input panel
        input_panel = Panel(
            f"[white]{text}[/white]",
            title="[cyan]Input Text[/cyan]",
            border_style=self.theme.secondary,
            box=ROUNDED
        )
        self.console.print(input_panel)
        
        # Hash result panel
        hash_panel = Panel(
            f"[bold cyan]{result}[/bold cyan]",
            title=f"[cyan]{hash_type} Hash[/cyan]",
            border_style=self.theme.primary,
            box=ROUNDED,
            padding=(1, 2)
        )
        self.console.print(hash_panel)
        self.console.print()
    
    def _display_all_hashes(self, text: str, results: Dict[str, str]) -> None:
        """Display all hash results"""
        self.console.print()
        
        # Input
        input_panel = Panel(
            f"[white]{text}[/white]",
            title="[cyan]Input Text[/cyan]",
            border_style=self.theme.secondary,
            box=ROUNDED
        )
        self.console.print(input_panel)
        self.console.print()
        
        # All hashes table
        table = Table(
            title="[bold cyan]Generated Hashes[/bold cyan]",
            box=ROUNDED,
            border_style=self.theme.primary
        )
        table.add_column("Algorithm", style="cyan", width=12)
        table.add_column("Hash Value", style="white")
        
        for algo, hash_value in results.items():
            table.add_row(algo, hash_value)
        
        self.console.print(table)
        self.console.print()
    
    def get_supported_hashes(self) -> list:
        """Get list of supported hash algorithms"""
        return list(self.SUPPORTED_HASHES.keys())
