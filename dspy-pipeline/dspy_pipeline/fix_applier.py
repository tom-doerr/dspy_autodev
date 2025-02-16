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
                with open(filename, 'r', encoding='utf8') as file:
                    content = file.read()

                # Only replace the first occurrence
                if search_block in content:
                    content = content.replace(search_block, replace_block, 1)

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
