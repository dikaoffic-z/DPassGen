"""
DPassGen Bulk Module
Bulk password generation functionality
"""

import json
import csv
from pathlib import Path
from typing import List
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
from rich.box import ROUNDED

from core.generator import PasswordGenerator
from ui.theme import CyberpunkTheme


class BulkModule:
    """Bulk password generation"""
    
    def __init__(self, console: Console, theme: CyberpunkTheme):
        self.console = console
        self.theme = theme
        self.generator = PasswordGenerator()
    
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
        """Generate multiple passwords"""
        passwords = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[cyan]{task.description}"),
            BarColumn(),
            TextColumn("[cyan]{task.completed}/{task.total}"),
            console=self.console
        ) as progress:
            task = progress.add_task("[cyan]Generating passwords...", total=count)
            
            for i in range(count):
                pwd = self.generator.generate(
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
                progress.update(task, advance=1)
        
        return passwords
    
    def export_txt(self, passwords: List[str], filename: str) -> str:
        """Export passwords to TXT file"""
        filepath = Path(filename).expanduser()
        with open(filepath, 'w') as f:
            for i, pwd in enumerate(passwords, 1):
                f.write(f"password_{i:04d}: {pwd}\n")
        
        return str(filepath.absolute())
    
    def export_json(self, passwords: List[str], filename: str) -> str:
        """Export passwords to JSON file"""
        filepath = Path(filename).expanduser()
        data = {
            "generator": "DPassGen",
            "count": len(passwords),
            "passwords": [
                {"index": i + 1, "password": pwd}
                for i, pwd in enumerate(passwords)
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return str(filepath.absolute())
    
    def export_csv(self, passwords: List[str], filename: str) -> str:
        """Export passwords to CSV file"""
        filepath = Path(filename).expanduser()
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["index", "password"])
            for i, pwd in enumerate(passwords, 1):
                writer.writerow([i, pwd])
        
        return str(filepath.absolute())
    
    def display_preview(self, passwords: List[str], limit: int = 10) -> None:
        """Display preview of generated passwords"""
        self.console.print()
        
        table = Table(
            title=f"[bold cyan]Generated Passwords ({len(passwords)} total)[/bold cyan]",
            box=ROUNDED,
            border_style=self.theme.primary
        )
        table.add_column("No.", style="cyan", width=8, justify="center")
        table.add_column("Password", style="white")
        
        display_count = min(limit, len(passwords))
        for i in range(display_count):
            table.add_row(str(i + 1), passwords[i])
        
        if len(passwords) > limit:
            table.add_row("...", "...")
            table.add_row(str(len(passwords)), f"[dim]({len(passwords) - limit} more...)[/dim]")
        
        self.console.print(table)
        self.console.print()
