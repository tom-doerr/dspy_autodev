import os
from rich.console import Console

console = Console()

class FixApplier:
    def apply_fix(self, filename: str, search_block: str, replace_block: str):
        # Prevent edits to autodev.py per guidelines from [jetbrains.com](https://www.jetbrains.com/guide/python/tips/move-block/)
        # and [computercraft.info](https://computercraft.info/wiki/Rename)
        if os.path.basename(filename) == "autodev.py":
            console.print("[red]Skipping modification of autodev.py. Please fix autodev.py manually.[/red]")
            return
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf8') as file:
                content = file.read()
            if search_block in content:
                content = content.replace(search_block, replace_block)
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
            console.print(f"[blue]Created new file {filename}.[/blue]")
