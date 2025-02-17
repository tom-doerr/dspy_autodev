import os
import logging
import re
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
                with open(filename, 'r', encoding='utf8') as file:
                    content = file.read()

                import re
                search_clean = search_block.strip()
                # First, try an exact match replacement.
                if search_clean in content:
                    content = content.replace(search_clean, replace_block, 1)
                else:
                    # Build a pattern that captures leading and trailing whitespace.
                    pattern = re.compile(r'(\s*)' + re.escape(search_clean) + r'(\s*)')
                    if re.search(pattern, content):
                        # Replace while preserving the surrounding whitespace.
                        content = re.sub(pattern, lambda m: m.group(1) + replace_block + m.group(2), content, count=1)
                    else:
                        console.print(f"[red]Search block not found in {filename}.[/red]")
                        console.print(f"[yellow]Expected search block:[/yellow] {search_block}")
                        console.print(f"[yellow]Replace block:[/yellow]")
                        console.print(replace_block)
                        return
   
                    with open(filename, 'w', encoding='utf8') as file:
                        file.write(content)
   
                    console.print(f"[green]Applied patch to {filename}.[/green]")
                else:
                    console.print(f"[red]Search block not found in {filename}.[/red]")
                    console.print(f"[yellow]Expected search block:[/yellow] {search_block}")
                    console.print(f"[yellow]Replace block:[/yellow]")
                    console.print(replace_block)

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
