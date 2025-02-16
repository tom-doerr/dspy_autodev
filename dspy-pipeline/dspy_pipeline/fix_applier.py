import os
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FixApplier:
    def apply_fix(self, filename: str, search_block: str, replace_block: str):
        # Prevent edits to autodev.py
        if os.path.basename(filename) == "autodev.py":
            from rich.console import Console
            console = Console()
            console.print("[red]Skipping modification of autodev.py. Please fix autodev.py manually.[/red]")
            return
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf8') as file:
                content = file.read()
            import re
            pattern = r'\b' + re.escape(search_block) + r'\b'
            from rich.console import Console
            console = Console()
            if re.search(pattern, content):
                content = re.sub(pattern, replace_block, content, count=1)
                with open(filename, 'w', encoding='utf8') as file:
                    file.write(content)
                console.print(f"[green]Applied patch to {filename}.[/green]")
            else:
                console.print(f"[red]Search block not found in {filename}.[/red]")
                console.print(f"[yellow]Expected search block:[/yellow] {search_block}")
                console.print(f"[yellow]Replace block:[/yellow]")
                console.print(replace_block)
        else:
            with open(filename, 'w', encoding='utf8') as file:
                file.write(replace_block)
            from rich.console import Console
            console = Console()
            console.print(f"[blue]Created new file {filename}.[/blue]")
