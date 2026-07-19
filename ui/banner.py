"""
DPassGen Banner Module
ASCII art banners and loading animations
"""

import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.live import Live
from rich.table import Table
from rich.box import ROUNDED

from .theme import CyberpunkTheme


class Banner:
    """ASCII art banners and loading screens"""
    
    ASCII_BANNER = """
██████╗ ██████╗  █████╗ ███████╗███████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝
██║  ██║██████╔╝███████║███████╗███████╗
██║  ██║██╔═══╝ ██╔══██║╚════██║╚════██║
██████╔╝██║     ██║  ██║███████║███████║
╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝
"""
    
    ASCII_BANNER_COMPACT = """
[bold cyan]██████╗ ██████╗  █████╗ ███████╗███████╗[/bold cyan]
[bold cyan]██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝[/bold cyan]
[bold cyan]██║  ██║██████╔╝███████║███████╗███████╗[/bold cyan]
[bold cyan]██║  ██║██╔═══╝ ██╔══██║╚════██║╚════██║[/bold cyan]
[bold cyan]██████╔╝██║     ██║  ██║███████║███████║[/bold cyan]
[bold cyan]╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝[/bold cyan]
"""
    
    def __init__(self, console: Console, theme: CyberpunkTheme):
        self.console = console
        self.theme = theme
    
    def show_splash(self, animated: bool = True) -> None:
        """Show splash screen with loading animation"""
        self.console.clear()
        
        # Show banner
        self._show_banner()
        
        if animated:
            # Loading animation
            self._show_loading()
        else:
            self.console.print()
    
    def _show_banner(self) -> None:
        """Display the ASCII banner"""
        self.console.print()
        
        # Main banner
        for line in self.ASCII_BANNER_COMPACT.split('\n'):
            if line.strip():
                self.console.print(line)
        
        # Subtitle
        self.console.print()
        self.console.print(Align.center(
            "[italic magenta]Secure Password Generator[/italic magenta]",
            width=60
        ))
        self.console.print()
    
    def _show_loading(self) -> None:
        """Show animated loading sequence"""
        loading_items = [
            "Loading Security Engine",
            "Loading Password Generator",
            "Loading Terminal UI",
            "Ready"
        ]
        
        loading_table = Table(
            box=ROUNDED,
            border_style="cyan",
            show_header=False,
            width=50
        )
        loading_table.add_column("Status", style="cyan", width=30)
        loading_table.add_column("Icon", style="green", width=3)
        
        for item in loading_items:
            time.sleep(0.3)
            loading_table.add_row(item, "✓")
            self.console.print(Align.center(loading_table, width=60))
            # Move cursor up to overwrite
            self.console.print("\033[F\033[F", end="")
        
        # Clear and show final
        self.console.print("\n\n")
        loading_table.add_row("[bold green]All systems ready![/bold green]", "[bold green]✓[/bold green]")
        self.console.print(Align.center(loading_table, width=60))
        
        time.sleep(0.5)
        self.console.clear()
    
    def show_main_banner(self) -> None:
        """Show main menu banner"""
        self.console.print()
        for line in self.ASCII_BANNER_COMPACT.split('\n'):
            if line.strip():
                self.console.print(Align.center(line, width=60))
        
        self.console.print(Align.center(
            "[bold magenta]╔══════════════════════════════════════╗[/bold magenta]",
            width=60
        ))
        self.console.print(Align.center(
            "[bold magenta]║[/bold magenta]      [bold cyan]Secure Password Generator[/bold cyan]        [bold magenta]║[/bold magenta]",
            width=60
        ))
        self.console.print(Align.center(
            "[bold magenta]╚══════════════════════════════════════╝[/bold magenta]",
            width=60
        ))
        self.console.print()
    
    def show_about_banner(self) -> None:
        """Show about section"""
        self.console.print()
        self.console.print(Align.center(
            "[bold cyan]═══════════════════════════════════════════[/bold cyan]",
            width=60
        ))
        self.console.print(Align.center(
            "[bold white]              ABOUT DPassGen[/bold white]",
            width=60
        ))
        self.console.print(Align.center(
            "[bold cyan]═══════════════════════════════════════════[/bold cyan]",
            width=60
        ))
        self.console.print()
    
    def animated_text(self, text: str, delay: float = 0.05) -> None:
        """Print text with typing animation"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    def pulse_text(self, text: str, times: int = 3) -> None:
        """Print pulsing text animation"""
        for _ in range(times):
            self.console.print(f"[bold cyan]{text}[/bold cyan]", end="\r")
            time.sleep(0.3)
            self.console.print(" " * len(text), end="\r")
            time.sleep(0.3)
        self.console.print(f"[bold cyan]{text}[/bold cyan]")
