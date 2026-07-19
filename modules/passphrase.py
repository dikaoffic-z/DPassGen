"""
DPassGen Passphrase Module
Passphrase generation functionality
"""

import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.box import ROUNDED

from core.generator import PasswordGenerator
from ui.theme import CyberpunkTheme


class PassphraseModule:
    """Passphrase generation"""
    
    def __init__(self, console: Console, theme: CyberpunkTheme, config: dict):
        self.console = console
        self.theme = theme
        self.config = config
        self.generator = PasswordGenerator()
    
    def generate_passphrase(
        self,
        word_count: int = 4,
        separator: str = "-",
        add_number: bool = True,
        capitalize: bool = True,
        copy_to_clipboard: bool = False
    ) -> str:
        """Generate a memorable passphrase"""
        passphrase = self.generator.generate_passphrase(
            word_count=word_count,
            separator=separator,
            add_number=add_number,
            capitalize=capitalize
        )
        
        # Display result
        self._display_passphrase_result(passphrase, word_count, separator)
        
        # Copy to clipboard if enabled
        if copy_to_clipboard or self.config.get("auto_copy", False):
            try:
                pyperclip.copy(passphrase)
                self.console.print(
                    self.theme.success("✓ Passphrase copied to clipboard!")
                )
            except:
                pass
        
        return passphrase
    
    def _display_passphrase_result(
        self,
        passphrase: str,
        word_count: int,
        separator: str
    ) -> None:
        """Display generated passphrase"""
        self.console.print()
        
        # Passphrase panel
        panel = Panel(
            f"[bold cyan]{passphrase}[/bold cyan]",
            title="[bold]Generated Passphrase[/bold]",
            border_style=self.theme.primary,
            box=ROUNDED,
            padding=(1, 2)
        )
        self.console.print(panel)
        
        # Stats
        table = Table(box=ROUNDED, border_style=self.theme.secondary)
        table.add_column("Metric", style="cyan", width=20)
        table.add_column("Value", style="white")
        
        words = passphrase.split(separator)
        table.add_row("Words", str(word_count))
        table.add_row("Total Length", str(len(passphrase)))
        table.add_row("Separator", separator)
        table.add_row("Has Numbers", "Yes" if any(c.isdigit() for c in passphrase) else "No")
        
        self.console.print(table)
        self.console.print()
