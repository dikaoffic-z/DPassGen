"""
DPassGen Password Module
Password generation functionality with UI
"""

import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.box import ROUNDED

from core.generator import PasswordGenerator
from core.analyzer import PasswordAnalyzer
from core.security import SecurityEngine
from ui.theme import CyberpunkTheme


class PasswordModule:
    """Password generation and management"""
    
    def __init__(self, console: Console, theme: CyberpunkTheme, config: dict):
        self.console = console
        self.theme = theme
        self.config = config
        self.generator = PasswordGenerator()
        self.analyzer = PasswordAnalyzer()
        self.security = SecurityEngine()
    
    def generate_password(
        self,
        length: int = 16,
        uppercase: bool = True,
        lowercase: bool = True,
        numbers: bool = True,
        symbols: bool = True,
        custom_chars: str = "",
        exclude_similar: bool = False,
        exclude_ambiguous: bool = False,
        copy_to_clipboard: bool = False
    ) -> str:
        """Generate a single secure password"""
        password = self.generator.generate(
            length=length,
            uppercase=uppercase,
            lowercase=lowercase,
            numbers=numbers,
            symbols=symbols,
            custom_chars=custom_chars,
            exclude_similar=exclude_similar,
            exclude_ambiguous=exclude_ambiguous
        )
        
        # Analyze password
        analysis = self.analyzer.analyze(password)
        
        # Display result
        self._display_password_result(password, analysis)
        
        # Copy to clipboard if enabled
        if copy_to_clipboard or self.config.get("auto_copy", False):
            try:
                pyperclip.copy(password)
                self.console.print(
                    self.theme.success("✓ Password copied to clipboard!")
                )
            except:
                pass
        
        return password
    
    def _display_password_result(self, password: str, analysis) -> None:
        """Display generated password with analysis"""
        self.console.print()
        
        # Password panel
        password_panel = Panel(
            f"[bold cyan]{password}[/bold cyan]",
            title="[bold]Generated Password[/bold]",
            border_style=self.theme.primary,
            box=ROUNDED,
            padding=(1, 2)
        )
        self.console.print(password_panel)
        
        # Stats table
        table = Table(box=ROUNDED, border_style=self.theme.secondary)
        table.add_column("Metric", style="cyan", width=20)
        table.add_column("Value", style="white")
        
        # Strength bar
        strength_bar = self._create_strength_bar(analysis.score)
        
        table.add_row("Strength", f"{strength_bar} {analysis.score}%")
        table.add_row("Entropy", f"{analysis.entropy:.1f} bits")
        table.add_row("Level", f"{analysis.strength_emoji} {analysis.strength_label}")
        table.add_row("Est. Crack Time", analysis.crack_time)
        
        self.console.print(table)
        
        # Character breakdown
        breakdown_table = Table(box=ROUNDED, border_style=self.theme.tertiary)
        breakdown_table.add_column("Type", style="cyan", width=15)
        breakdown_table.add_column("Count", style="white", justify="center")
        
        bd = analysis.character_breakdown
        breakdown_table.add_row("Uppercase", str(bd.get("uppercase", 0)))
        breakdown_table.add_row("Lowercase", str(bd.get("lowercase", 0)))
        breakdown_table.add_row("Numbers", str(bd.get("numbers", 0)))
        breakdown_table.add_row("Symbols", str(bd.get("symbols", 0)))
        breakdown_table.add_row("Other", str(bd.get("other", 0)))
        
        self.console.print(breakdown_table)
        self.console.print()
    
    def _create_strength_bar(self, score: int) -> str:
        """Create a visual strength bar"""
        filled = int(score / 10)
        empty = 10 - filled
        
        if score < 40:
            color = "red"
        elif score < 70:
            color = "yellow"
        else:
            color = "green"
        
        return f"[{color}]{'█' * filled}[/{color}]{'░' * empty}"
