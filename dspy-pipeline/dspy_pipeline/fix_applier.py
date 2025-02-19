import os
import logging
from rich.console import Console

console = Console()

class FixApplier:
    def apply_fix(self, filename: str, search_block: str, replace_block: str):
        """
        Applies a fix by replacing a search block with a replace block in a given file.
        """
        # Prevent edits to autodev.py
        if os.path.basename(filename) == "autodev.py":
            console.print("[red]Skipping modification of autodev.py. Please fix autodev.py manually.[/red]")
            return

        if os.path.exists(filename):
            try:
                import re
                with open(filename, "r", encoding="utf8") as f:
                    content = f.read()
                search_clean = search_block.strip()
                if search_clean in content:
                    new_content = content.replace(search_clean, replace_block, 1)
                    count = 1
                else:
                    pattern = re.compile(r'(\s*)' + re.escape(search_clean) + r'(\s*)')
                    new_content, count = re.subn(pattern, lambda m: m.group(1) + replace_block + m.group(2), content, count=1)
                if count:
                     with open(filename, "w", newline="") as f:
                          f.write(new_content)
                console.print(f"[green]Applied patch to {filename}.[/green]")

            except FileNotFoundError:
                logging.error(f"File not found: {filename}")
            except Exception as e:
                logging.error(f"Error applying fix to {filename}: {e}")
        else:
            try:
                with open(filename, 'w', encoding='utf8') as file:
                    file.write(replace_block)
                console.print(f"[blue]Created new file {filename}.[/blue]")
            except Exception as e:
                logging.error(f"Error creating new file {filename}: {e}")
