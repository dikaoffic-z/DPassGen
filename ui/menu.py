"""
DPassGen Menu Module
Interactive menu system with arrow navigation
"""

from typing import List, Callable, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.box import ROUNDED
from rich.align import Align
import questionary

from .theme import CyberpunkTheme
from .banner import Banner


class MenuItem:
    """Represents a menu item"""
    
    def __init__(self, key: str, icon: str, title: str, description: str = ""):
        self.key = key
        self.icon = icon
        self.title = title
        self.description = description
    
    def __str__(self):
        return f"{self.icon} {self.title}"


class InteractiveMenu:
    """Interactive menu system with arrow key navigation"""
    
    MENU_ITEMS = [
        MenuItem("1", "🔐", "Generate Password", "Generate a secure password"),
        MenuItem("2", "📦", "Bulk Password Generator", "Generate multiple passwords at once"),
        MenuItem("3", "💪", "Password Strength Checker", "Check password strength and security"),
        MenuItem("4", "🔎", "Password Analyzer", "Analyze password for vulnerabilities"),
        MenuItem("5", "📝", "Passphrase Generator", "Generate memorable passphrases"),
        MenuItem("6", "🔑", "Hash Generator", "Generate cryptographic hashes"),
        MenuItem("7", "⚙", "Settings", "Configure application settings"),
        MenuItem("8", "ℹ", "About", "About DPassGen"),
        MenuItem("0", "🚪", "Exit", "Exit the application"),
    ]
    
    def __init__(self, console: Console, theme: CyberpunkTheme, banner: Banner):
        self.console = console
        self.theme = theme
        self.banner = banner
    
    def show_main_menu(self) -> str:
        """Display main menu and return selected option"""
        self.console.clear()
        self.banner.show_main_banner()
        
        # Create menu panel with fixed width
        menu_lines = []
        for item in self.MENU_ITEMS:
            key_str = f"[{item.key}]"
            desc = item.description if item.description else ""
            menu_lines.append(f"{key_str} {item.icon} {item.title:<28} {desc}")
        
        menu_text = "\n".join(menu_lines)
        menu_panel = Panel(
            f"[cyan]{menu_text}[/cyan]",
            box=ROUNDED,
            border_style="cyan",
            padding=(1, 2),
            width=70
        )
        
        self.console.print(Align.center(menu_panel, width=75))
        self.console.print()
        self.console.print(Align.center(
            "[dim]Use arrow keys to navigate, Enter to select[/dim]",
            width=60
        ))
        self.console.print()
        
        # Use questionary for interactive selection
        choices = [f"{item.icon} {item.title}" for item in self.MENU_ITEMS]
        
        selected = questionary.select(
            "Select an option:",
            choices=choices,
            style=questionary.Style([
                ('selected', 'fg:cyan bold'),
                ('choice', 'fg:white'),
                ('pointer', 'fg:cyan bold'),
            ])
        ).ask()
        
        # Find selected item
        for item in self.MENU_ITEMS:
            if f"{item.icon} {item.title}" == selected:
                return item.key
        
        return "0"
    
    def show_submenu(self, title: str, items: List[str]) -> Optional[int]:
        """Show a simple submenu"""
        self.console.print()
        
        table = Table(
            box=ROUNDED,
            border_style="cyan",
            show_header=False,
            width=40
        )
        table.add_column("No.", style="cyan bold", width=5)
        table.add_column("Option", style="white")
        
        for i, item in enumerate(items, 1):
            table.add_row(f"{i}.", item)
        
        self.console.print(Align.center(table, width=50))
        
        return None
    
    def confirm_action(self, message: str) -> bool:
        """Ask for confirmation"""
        return questionary.confirm(
            message,
            style=questionary.Style([
                ('selected', 'fg:cyan bold'),
                ('confirm', 'fg:green'),
                ('cancel', 'fg:red'),
            ])
        ).ask()
    
    def input_text(self, message: str, default: str = "") -> str:
        """Get text input from user"""
        result = questionary.text(
            message,
            default=default,
            style=questionary.Style([
                ('input', 'fg:white'),
                ('pointer', 'fg:cyan bold'),
            ])
        ).ask()
        
        return result if result else default
    
    def select_choice(self, message: str, choices: List[str]) -> str:
        """Select from a list of choices"""
        return questionary.select(
            message,
            choices=choices,
            style=questionary.Style([
                ('selected', 'fg:cyan bold'),
                ('choice', 'fg:white'),
                ('pointer', 'fg:cyan bold'),
            ])
        ).ask()
    
    def select_multiple(self, message: str, choices: List[str], default: List[str] = None) -> List[str]:
        """Select multiple options"""
        # Format choices with checked state
        formatted_choices = []
        for choice in choices:
            is_checked = default and choice in default
            formatted_choices.append(questionary.Choice(choice, checked=is_checked))
        
        return questionary.checkbox(
            message,
            choices=formatted_choices,
            style=questionary.Style([
                ('selected', 'fg:cyan bold'),
                ('checkbox', 'fg:cyan'),
                ('pointer', 'fg:cyan bold'),
            ])
        ).ask()
