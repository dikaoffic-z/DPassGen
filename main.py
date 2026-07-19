#!/usr/bin/env python3
"""
DPassGen - Secure Password Generator CLI
A premium, cyberpunk-themed password generator for terminal
"""

import sys
import argparse
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.box import ROUNDED
from rich.align import Align
from rich.syntax import Syntax

from ui.theme import CyberpunkTheme
from ui.banner import Banner
from ui.menu import InteractiveMenu
from core.generator import PasswordGenerator
from core.analyzer import PasswordAnalyzer
from core.security import SecurityEngine
from modules.password import PasswordModule
from modules.bulk import BulkModule
from modules.passphrase import PassphraseModule
from modules.hash import HashModule
from utils.helper import ConfigManager


class DPassGenApp:
    """Main DPassGen Application"""
    
    VERSION = "1.0.0"
    AUTHOR = "DIKA OFFICIAL"
    
    def __init__(self, args=None):
        self.args = args or argparse.Namespace()
        self.console = Console(theme=CyberpunkTheme.rich_theme)
        self.theme = CyberpunkTheme()
        self.theme.set_console(self.console)
        self.banner = Banner(self.console, self.theme)
        self.config = ConfigManager()
        self.menu = InteractiveMenu(self.console, self.theme, self.banner)
        
        # Initialize modules
        self.password_module = PasswordModule(self.console, self.theme, self.config.get_all())
        self.bulk_module = BulkModule(self.console, self.theme)
        self.passphrase_module = PassphraseModule(self.console, self.theme, self.config.get_all())
        self.hash_module = HashModule(self.console, self.theme, self.config.get_all())
        self.generator = PasswordGenerator()
        self.analyzer = PasswordAnalyzer()
    
    def run(self) -> None:
        """Run the application"""
        # Show splash screen
        animated = self.config.get("animation", True)
        self.banner.show_splash(animated=animated)
        
        # Handle command line arguments
        if hasattr(self.args, 'generate') and self.args.generate:
            self._handle_generate()
        elif hasattr(self.args, 'strength') and self.args.strength:
            self._handle_strength_check(self.args.strength)
        elif hasattr(self.args, 'hash') and self.args.hash:
            self._handle_hash(self.args.hash)
        elif hasattr(self.args, 'passphrase') and self.args.passphrase:
            self._handle_passphrase()
        else:
            # Run interactive mode
            self._run_interactive()
    
    def _run_interactive(self) -> None:
        """Run interactive menu mode"""
        while True:
            choice = self.menu.show_main_menu()
            
            if choice == "1":
                self._menu_generate_password()
            elif choice == "2":
                self._menu_bulk_generator()
            elif choice == "3":
                self._menu_strength_checker()
            elif choice == "4":
                self._menu_password_analyzer()
            elif choice == "5":
                self._menu_passphrase_generator()
            elif choice == "6":
                self._menu_hash_generator()
            elif choice == "7":
                self._menu_settings()
            elif choice == "8":
                self._menu_about()
            elif choice == "0":
                self._exit_app()
                break
    
    def _menu_generate_password(self) -> None:
        """Generate password menu"""
        self.console.clear()
        self.console.print(Align.center("[bold cyan]🔐 Generate Password[/bold cyan]\n", width=60))
        
        # Get password length
        length_str = self.menu.input_text("Password length (4-2048):", str(self.config.get("default_length", 16)))
        try:
            length = max(4, min(2048, int(length_str)))
        except ValueError:
            length = 16
        
        # Character options
        char_options = self.menu.select_multiple(
            "Select character types:",
            ["Uppercase (A-Z)", "Lowercase (a-z)", "Numbers (0-9)", "Symbols (!@#$%)"],
            default=["Uppercase (A-Z)", "Lowercase (a-z)", "Numbers (0-9)", "Symbols (!@#$%)"]
        )
        
        uppercase = "Uppercase (A-Z)" in char_options
        lowercase = "Lowercase (a-z)" in char_options
        numbers = "Numbers (0-9)" in char_options
        symbols = "Symbols (!@#$%)" in char_options
        
        # Custom characters
        custom_chars = ""
        use_custom = self.menu.confirm_action("Add custom characters?")
        if use_custom:
            custom_chars = self.menu.input_text("Enter custom characters:", "")
        
        # Exclude options
        exclude_similar = self.menu.confirm_action("Exclude similar characters (i,l,1,O,0)?")
        exclude_ambiguous = self.menu.confirm_action("Exclude ambiguous characters?")
        
        # Copy option
        copy = self.menu.confirm_action("Copy to clipboard?")
        
        self.console.print()
        
        # Validate at least one character type is selected
        if not any([uppercase, lowercase, numbers, symbols]) and not custom_chars:
            self.console.print(self.theme.error("✖ Error: Please select at least one character type!"))
            self._press_enter_to_continue()
            return
        
        # Generate password with error handling
        try:
            self.password_module.generate_password(
                length=length,
                uppercase=uppercase,
                lowercase=lowercase,
                numbers=numbers,
                symbols=symbols,
                custom_chars=custom_chars,
                exclude_similar=exclude_similar,
                exclude_ambiguous=exclude_ambiguous,
                copy_to_clipboard=copy
            )
        except ValueError as e:
            self.console.print(self.theme.error(f"✖ Error: {str(e)}"))
        except Exception as e:
            self.console.print(self.theme.error(f"✖ Unexpected error: {str(e)}"))
        
        self._press_enter_to_continue()
    
    def _menu_bulk_generator(self) -> None:
        """Bulk password generator menu"""
        self.console.clear()
        self.console.print(Align.center("[bold cyan]📦 Bulk Password Generator[/bold cyan]\n", width=60))
        
        # Select count
        count_choice = self.menu.select_choice(
            "How many passwords to generate?",
            ["10", "50", "100", "500", "1000"]
        )
        count = int(count_choice)
        
        # Get password length
        length_str = self.menu.input_text("Password length (4-2048):", "16")
        try:
            length = max(4, min(2048, int(length_str)))
        except ValueError:
            length = 16
        
        # Character options
        char_options = self.menu.select_multiple(
            "Select character types:",
            ["Uppercase (A-Z)", "Lowercase (a-z)", "Numbers (0-9)", "Symbols (!@#$%)"],
            default=["Uppercase (A-Z)", "Lowercase (a-z)", "Numbers (0-9)", "Symbols (!@#$%)"]
        )
        
        uppercase = "Uppercase (A-Z)" in char_options
        lowercase = "Lowercase (a-z)" in char_options
        numbers = "Numbers (0-9)" in char_options
        symbols = "Symbols (!@#$%)" in char_options
        
        # Prefix option
        prefix = ""
        use_prefix = self.menu.confirm_action("Add prefix to passwords?")
        if use_prefix:
            prefix = self.menu.input_text("Enter prefix:", "pass_")
        
        self.console.print()
        
        # Validate at least one character type is selected
        if not any([uppercase, lowercase, numbers, symbols]):
            self.console.print(self.theme.error("✖ Error: Please select at least one character type!"))
            self._press_enter_to_continue()
            return
        
        # Generate passwords with error handling
        try:
            passwords = self.bulk_module.generate_bulk(
                count=count,
                length=length,
                uppercase=uppercase,
                lowercase=lowercase,
                numbers=numbers,
                symbols=symbols,
                prefix=prefix
            )
        except ValueError as e:
            self.console.print(self.theme.error(f"✖ Error: {str(e)}"))
            self._press_enter_to_continue()
            return
        except Exception as e:
            self.console.print(self.theme.error(f"✖ Unexpected error: {str(e)}"))
            self._press_enter_to_continue()
            return
        
        # Display preview
        self.bulk_module.display_preview(passwords)
        
        # Export option
        export = self.menu.confirm_action("Export passwords?")
        if export:
            export_format = self.menu.select_choice(
                "Select export format:",
                ["TXT", "JSON", "CSV"]
            )
            
            filename = self.menu.input_text("Enter filename:", f"passwords.{export_format.lower()}")
            
            if export_format == "TXT":
                filepath = self.bulk_module.export_txt(passwords, filename)
            elif export_format == "JSON":
                filepath = self.bulk_module.export_json(passwords, filename)
            else:
                filepath = self.bulk_module.export_csv(passwords, filename)
            
            self.console.print(self.theme.success(f"✓ Exported to {filepath}"))
        
        self._press_enter_to_continue()
    
    def _menu_strength_checker(self) -> None:
        """Password strength checker menu"""
        self.console.clear()
        self.console.print(Align.center("[bold cyan]💪 Password Strength Checker[/bold cyan]\n", width=60))
        
        password = self.menu.input_text("Enter password to check:")
        
        if password:
            analysis = self.analyzer.analyze(password)
            
            self.console.print()
            
            # Strength panel
            strength_emoji = analysis.strength_emoji
            strength_label = analysis.strength_label
            strength_color = "green" if analysis.score >= 70 else "yellow" if analysis.score >= 40 else "red"
            
            panel = Panel(
                f"[bold {strength_color}]{strength_emoji} {strength_label}[/bold {strength_color}]",
                title="[cyan]Strength Level[/cyan]",
                border_style="cyan",
                box=ROUNDED
            )
            self.console.print(panel)
            
            # Stats table
            table = Table(box=ROUNDED, border_style="cyan")
            table.add_column("Metric", style="cyan", width=20)
            table.add_column("Value", style="white")
            
            table.add_row("Score", f"{analysis.score}/100")
            table.add_row("Entropy", f"{analysis.entropy:.1f} bits")
            table.add_row("Est. Crack Time", analysis.crack_time)
            table.add_row("Length", str(len(password)))
            
            self.console.print(table)
            
            # Strength bar
            filled = int(analysis.score / 10)
            bar = f"[{'green' if analysis.score >= 70 else 'yellow' if analysis.score >= 40 else 'red'}]{'█' * filled}[/{'green' if analysis.score >= 70 else 'yellow' if analysis.score >= 40 else 'red'}]{'░' * (10 - filled)}"
            self.console.print(f"\n[cyan]Strength:[/cyan] {bar} {analysis.score}%")
            
            # Issues
            if analysis.issues:
                self.console.print("\n[red]Issues found:[/red]")
                for issue in analysis.issues:
                    self.console.print(f"  [red]✖[/red] {issue}")
            
            # Recommendations
            if analysis.recommendations:
                self.console.print("\n[green]Recommendations:[/green]")
                for rec in analysis.recommendations:
                    self.console.print(f"  [green]✓[/green] {rec}")
        
        self._press_enter_to_continue()
    
    def _menu_password_analyzer(self) -> None:
        """Password analyzer menu"""
        self.console.clear()
        self.console.print(Align.center("[bold cyan]🔎 Password Analyzer[/bold cyan]\n", width=60))
        
        password = self.menu.input_text("Enter password to analyze:")
        
        if password:
            self._analyze_password_detail(password)
        
        self._press_enter_to_continue()
    
    def _analyze_password_detail(self, password: str) -> None:
        """Detailed password analysis"""
        analysis = self.analyzer.analyze(password)
        
        self.console.print()
        
        # Character breakdown
        table = Table(
            title="[bold cyan]Character Breakdown[/bold cyan]",
            box=ROUNDED,
            border_style="cyan"
        )
        table.add_column("Type", style="cyan", width=15)
        table.add_column("Count", style="white", justify="center")
        
        bd = analysis.character_breakdown
        table.add_row("Uppercase", str(bd.get("uppercase", 0)))
        table.add_row("Lowercase", str(bd.get("lowercase", 0)))
        table.add_row("Numbers", str(bd.get("numbers", 0)))
        table.add_row("Symbols", str(bd.get("symbols", 0)))
        table.add_row("Total Length", str(len(password)))
        
        self.console.print(table)
        
        # Security analysis
        self.console.print("\n[bold cyan]Security Analysis:[/bold cyan]")
        
        checks = [
            ("Password length >= 8", len(password) >= 8),
            ("Password length >= 12", len(password) >= 12),
            ("Contains uppercase", bd.get("uppercase", 0) > 0),
            ("Contains lowercase", bd.get("lowercase", 0) > 0),
            ("Contains numbers", bd.get("numbers", 0) > 0),
            ("Contains symbols", bd.get("symbols", 0) > 0),
            ("No sequential patterns", len(analysis.issues) == 0),
        ]
        
        for check_name, passed in checks:
            status = "[green]✓ Pass[/green]" if passed else "[red]✗ Fail[/red]"
            self.console.print(f"  {status} - {check_name}")
    
    def _menu_passphrase_generator(self) -> None:
        """Passphrase generator menu"""
        self.console.clear()
        self.console.print(Align.center("[bold cyan]📝 Passphrase Generator[/bold cyan]\n", width=60))
        
        # Word count
        word_count_choice = self.menu.select_choice(
            "Number of words:",
            ["3 words", "4 words", "5 words", "6 words"]
        )
        word_count = int(word_count_choice.split()[0])
        
        # Separator
        separator = self.menu.input_text("Separator (default: -):", "-")
        if not separator:
            separator = "-"
        
        # Options
        add_number = self.menu.confirm_action("Add random number at end?")
        capitalize = self.menu.confirm_action("Capitalize words?")
        copy = self.menu.confirm_action("Copy to clipboard?")
        
        self.console.print()
        
        # Generate passphrase
        passphrase = self.passphrase_module.generate_passphrase(
            word_count=word_count,
            separator=separator,
            add_number=add_number,
            capitalize=capitalize,
            copy_to_clipboard=copy
        )
        
        self._press_enter_to_continue()
    
    def _menu_hash_generator(self) -> None:
        """Hash generator menu"""
        self.console.clear()
        self.console.print(Align.center("[bold cyan]🔑 Hash Generator[/bold cyan]\n", width=60))
        
        # Input text
        text = self.menu.input_text("Enter text to hash:")
        
        if text:
            # Hash type selection
            hash_choice = self.menu.select_choice(
                "Select hash algorithm:",
                ["MD5", "SHA1", "SHA256", "SHA384", "SHA512", "All Hashes"]
            )
            
            self.console.print()
            
            if hash_choice == "All Hashes":
                self.hash_module.generate_all_hashes(text)
            else:
                self.hash_module.generate_hash(text, hash_choice.lower())
        
        self._press_enter_to_continue()
    
    def _menu_settings(self) -> None:
        """Settings menu"""
        self.console.clear()
        self.console.print(Align.center("[bold cyan]⚙ Settings[/bold cyan]\n", width=60))
        
        settings_table = Table(
            title="[bold cyan]Current Settings[/bold cyan]",
            box=ROUNDED,
            border_style="cyan"
        )
        settings_table.add_column("Setting", style="cyan", width=25)
        settings_table.add_column("Value", style="white")
        
        config = self.config.get_all()
        settings_table.add_row("Default Length", str(config.get("default_length", 16)))
        settings_table.add_row("Theme", config.get("theme", "cyberpunk"))
        settings_table.add_row("Animation", "Enabled" if config.get("animation", True) else "Disabled")
        settings_table.add_row("Auto Copy", "Enabled" if config.get("auto_copy", False) else "Disabled")
        settings_table.add_row("Exclude Similar", "Yes" if config.get("exclude_similar", False) else "No")
        settings_table.add_row("Exclude Ambiguous", "Yes" if config.get("exclude_ambiguous", False) else "No")
        
        self.console.print(settings_table)
        self.console.print()
        
        # Settings options
        setting_choice = self.menu.select_choice(
            "Select setting to modify:",
            ["Default Length", "Animation", "Auto Copy", "Exclude Similar", "Exclude Ambiguous", "Reset to Defaults", "Back"]
        )
        
        if setting_choice == "Default Length":
            length = self.menu.input_text("Enter default length (4-2048):", str(config.get("default_length", 16)))
            try:
                self.config.set("default_length", max(4, min(2048, int(length))))
                self.console.print(self.theme.success("✓ Default length updated"))
            except ValueError:
                self.console.print(self.theme.error("✖ Invalid length"))
        
        elif setting_choice == "Animation":
            enabled = self.menu.confirm_action("Enable loading animations?")
            self.config.set("animation", enabled)
            self.console.print(self.theme.success("✓ Animation setting updated"))
        
        elif setting_choice == "Auto Copy":
            enabled = self.menu.confirm_action("Enable auto copy to clipboard?")
            self.config.set("auto_copy", enabled)
            self.console.print(self.theme.success("✓ Auto copy setting updated"))
        
        elif setting_choice == "Exclude Similar":
            enabled = self.menu.confirm_action("Exclude similar characters by default?")
            self.config.set("exclude_similar", enabled)
            self.console.print(self.theme.success("✓ Exclude similar setting updated"))
        
        elif setting_choice == "Exclude Ambiguous":
            enabled = self.menu.confirm_action("Exclude ambiguous characters by default?")
            self.config.set("exclude_ambiguous", enabled)
            self.console.print(self.theme.success("✓ Exclude ambiguous setting updated"))
        
        elif setting_choice == "Reset to Defaults":
            if self.menu.confirm_action("Reset all settings to defaults?"):
                self.config.reset()
                self.console.print(self.theme.success("✓ Settings reset to defaults"))
    
    def _menu_about(self) -> None:
        """About menu"""
        self.console.clear()
        self.banner.show_about_banner()
        
        # About info
        table = Table(box=ROUNDED, border_style="cyan", width=50)
        table.add_column("Info", style="cyan", width=15)
        table.add_column("Value", style="white")
        
        table.add_row("Name", "DPassGen")
        table.add_row("Version", self.VERSION)
        table.add_row("Developer", self.AUTHOR)
        table.add_row("Type", "Secure Password Generator")
        
        self.console.print(Align.center(table, width=60))
        
        # Features
        self.console.print("\n[bold cyan]Features:[/bold cyan]")
        features = [
            "🔐 Secure password generation",
            "📦 Bulk password generator",
            "💪 Password strength checker",
            "🔎 Password analyzer",
            "📝 Passphrase generator",
            "🔑 Hash generator",
            "⚙ Configurable settings",
            "🎨 Cyberpunk theme UI"
        ]
        
        for feature in features:
            self.console.print(f"  {feature}")
        
        # Security info
        self.console.print("\n[bold yellow]Security:[/bold yellow]")
        self.console.print("  Uses Python's secrets module for cryptographic security")
        self.console.print("  No password storage - all passwords in memory only")
        
        self._press_enter_to_continue()
    
    def _exit_app(self) -> None:
        """Exit the application"""
        self.console.clear()
        self.console.print()
        self.console.print(Align.center("[bold cyan]Thank you for using DPassGen![/bold cyan]", width=60))
        self.console.print(Align.center("[dim]Stay secure, stay safe.[/dim]\n", width=60))
        time.sleep(1)
    
    def _press_enter_to_continue(self) -> None:
        """Wait for user to press enter"""
        self.console.print()
        self.menu.input_text("Press Enter to continue...")
    
    def _handle_generate(self) -> None:
        """Handle --generate argument"""
        length = getattr(self.args, 'length', 16)
        self.password_module.generate_password(length=length)
    
    def _handle_strength_check(self, password: str) -> None:
        """Handle --strength argument"""
        if password:
            analysis = self.analyzer.analyze(password)
            self.console.print(f"\n[cyan]Password:[/cyan] {password}")
            self.console.print(f"[cyan]Strength:[/cyan] {analysis.strength_emoji} {analysis.strength_label}")
            self.console.print(f"[cyan]Score:[/cyan] {analysis.score}/100")
            self.console.print(f"[cyan]Entropy:[/cyan] {analysis.entropy:.1f} bits")
            self.console.print(f"[cyan]Est. Crack Time:[/cyan] {analysis.crack_time}")
        else:
            self.console.print(self.theme.error("✖ Please provide a password to check"))
    
    def _handle_hash(self, text: str) -> None:
        """Handle --hash argument"""
        if text:
            hash_type = getattr(self.args, 'type', 'sha256')
            result = self.hash_module.generate_hash(text, hash_type)
            self.console.print(f"\n[cyan]{hash_type.upper()} Hash:[/cyan] {result}")
        else:
            self.console.print(self.theme.error("✖ Please provide text to hash"))
    
    def _handle_passphrase(self) -> None:
        """Handle --passphrase argument"""
        word_count = getattr(self.args, 'words', 4)
        passphrase = self.generator.generate_passphrase(word_count=word_count)
        self.console.print(f"\n[cyan]Passphrase:[/cyan] {passphrase}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="DPassGen - Secure Password Generator CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--generate", "-g",
        action="store_true",
        help="Generate a single password"
    )
    parser.add_argument(
        "--length", "-l",
        type=int,
        default=16,
        help="Password length (default: 16)"
    )
    parser.add_argument(
        "--strength", "-s",
        type=str,
        metavar="PASSWORD",
        help="Check password strength"
    )
    parser.add_argument(
        "--hash",
        type=str,
        metavar="TEXT",
        help="Generate hash of text"
    )
    parser.add_argument(
        "--type",
        type=str,
        default="sha256",
        choices=["md5", "sha1", "sha256", "sha384", "sha512"],
        help="Hash type (default: sha256)"
    )
    parser.add_argument(
        "--passphrase", "-p",
        action="store_true",
        help="Generate a passphrase"
    )
    parser.add_argument(
        "--words", "-w",
        type=int,
        default=4,
        help="Number of words for passphrase (default: 4)"
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="DPassGen v1.0.0"
    )
    
    args = parser.parse_args()
    
    try:
        app = DPassGenApp(args)
        app.run()
    except KeyboardInterrupt:
        print("\n\n[cyan]Goodbye![/cyan]")
        sys.exit(0)
    except Exception as e:
        console = Console()
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
