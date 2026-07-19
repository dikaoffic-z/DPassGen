"""
DPassGen Theme Module
Cyberpunk theme and color definitions
"""

from rich.style import Style
from rich.theme import Theme


class CyberpunkTheme:
    """Cyberpunk themed colors and styles for DPassGen"""
    
    # Primary colors
    primary = "cyan"
    secondary = "magenta"
    tertiary = "purple"
    
    # Status colors
    success = "green"
    warning = "yellow"
    error = "red"
    info = "blue"
    
    # Text colors
    text = "white"
    dim = "dim"
    
    # Gradient colors for banners
    gradient_colors = ["cyan", "magenta", "purple", "blue"]
    
    # Custom theme for Rich
    rich_theme = Theme({
        "primary": "cyan",
        "secondary": "magenta bold",
        "success": "green bold",
        "warning": "yellow bold",
        "error": "red bold",
        "info": "blue bold",
        "title": "bold cyan",
        "subtitle": "italic magenta",
        "dim": "dim",
    })
    
    def __init__(self):
        self.console = None
    
    def set_console(self, console):
        """Set console instance"""
        self.console = console
    
    def success(self, message: str) -> str:
        """Format success message"""
        return f"[green]✔[/green] {message}"
    
    def error(self, message: str) -> str:
        """Format error message"""
        return f"[red]✖[/red] {message}"
    
    def warning(self, message: str) -> str:
        """Format warning message"""
        return f"[yellow]⚠[/yellow] {message}"
    
    def info(self, message: str) -> str:
        """Format info message"""
        return f"[blue]ℹ[/blue] {message}"
    
    def header(self, text: str) -> str:
        """Format header text"""
        return f"[bold cyan]{text}[/bold cyan]"
    
    def subheader(self, text: str) -> str:
        """Format subheader text"""
        return f"[italic magenta]{text}[/italic magenta]"
    
    def bullet(self, text: str) -> str:
        """Format bullet point"""
        return f"[cyan]▸[/cyan] {text}"
    
    def checkmark(self, text: str) -> str:
        """Format checkmark item"""
        return f"[green]✓[/green] {text}"
    
    def crossmark(self, text: str) -> str:
        """Format crossmark item"""
        return f"[red]✗[/red] {text}"
    
    def divider(self, char: str = "─", length: int = 50) -> str:
        """Create a divider line"""
        return char * length
    
    def box_top(self, title: str = "", width: int = 50) -> str:
        """Create box top with optional title"""
        if title:
            padding = (width - len(title) - 4) // 2
            return f"╔{'═' * padding} {title} {'═' * (width - len(title) - 4 - padding)}╗"
        return f"╔{'═' * (width - 2)}╗"
    
    def box_bottom(self, width: int = 50) -> str:
        """Create box bottom"""
        return f"╚{'═' * (width - 2)}╝"
    
    def box_side(self) -> str:
        """Create box side"""
        return "║"
    
    def create_gradient_text(self, text: str) -> str:
        """Create gradient effect text (for terminal without true color)"""
        return f"[cyan]{text}[/cyan]"
    
    def get_banner_style(self) -> dict:
        """Get banner styling dictionary"""
        return {
            "color": "cyan",
            "style": "bold",
            "border_style": "cyan"
        }
