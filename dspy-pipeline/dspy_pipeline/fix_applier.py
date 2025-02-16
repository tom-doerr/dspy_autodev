import os
import subprocess
import time
import dspy
from dspy_pipeline.utils import helper_function
try:
    from rich.console import Console
except ImportError:
    print("Rich module not installed. Please run 'poetry install' in the dspy-pipeline directory.")
    exit(1)
console = Console()
import sys
import os

def run_autodev():
    result = subprocess.run(
        ['python', 'autodev.py'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        console.print("[red]Error encountered while running autodev.py:[/red]")
        console.print("[yellow]stderr:[/yellow]")
        console.print(result.stderr)
    return result.returncode, result.stdout, result.stderr

def gather_code_contents():
    combined = ""
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs:
            dirs.remove('.git')
        for f in files:
            if f in ['LICENSE', '.gitignore']:
                continue
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf8', errors='replace') as file:
                combined += f"{path}:\n" + file.read() + "\n\n"
    return combined

def get_fix_instructions(code_text: str, error_text: str):
    from dspy_pipeline.fix_module import FixModule
    fix_module = FixModule()
    fix_result = fix_module.forward(code_text, error_text)
    return fix_result.filename, fix_result.search, fix_result.replace

def apply_fix(filename: str, search_block: str, replace_block: str):
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
