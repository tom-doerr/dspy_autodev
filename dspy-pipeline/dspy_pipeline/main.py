import os
import subprocess
import time
from dspy_pipeline.utils import helper_function
try:
    from rich.console import Console
except ImportError:
    print("Rich module not installed. Please run 'poetry install' in the dspy-pipeline directory.")
    exit(1)
console = Console()
import sys

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

def get_fix_instructions(code_text, error_text):
    from dspy_pipeline.fix_module import FixModule
    fix_module = FixModule()
    fix_result = fix_module.forward(code_text, error_text)
    return fix_result["filename"], fix_result["search"], fix_result["replace"]

def apply_fix(filename, search_block, replace_block):
    # Prevent edits to autodev.py per guidelines from [jetbrains.com](https://www.jetbrains.com/guide/python/tips/move-block/) 
    # and [computercraft.info](https://computercraft.info/wiki/Rename)
    if filename == "autodev.py":
        console.print("[red]Skipping modification of autodev.py. Please fix autodev.py manually.[/red]")
        return
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf8') as file:
            content = file.read()
        if search_block in content:
            content = content.replace(search_block, replace_block, 1)
            with open(filename, 'w', encoding='utf8') as file:
                file.write(content)
            console.print(f"[green]Applied patch to {filename}.[/green]")
        else:
            console.print(f"[red]Search block not found in {filename}.[/red]")
            console.print(f"[yellow]Expected search block:[/yellow] {search_block}")
            console.print(f"[yellow]Replace block:[/yellow] {replace_block}")
    else:
        with open(filename, 'w', encoding='utf8') as file:
            file.write(replace_block)
        console.print(f"[blue]Created new file {filename}.[/blue]")

def main_loop():
    last_mod_time = os.path.getmtime('autodev.py') if os.path.exists('autodev.py') else 0
    try:
        while True:
            retcode, stdout, stderr = run_autodev()
            if retcode != 0 or stderr.strip():
                console.print("[red]Error encountered while running autodev.py[/red]")
                console.print("[yellow]Error details:[/yellow]")
                console.print(stderr if stderr.strip() else stdout)
                try:
                    with open('autodev.py', 'r', encoding='utf8') as f:
                        autodev_source = f.read()
                except Exception as e:
                    autodev_source = "Could not read autodev.py: " + str(e)
                code_contents = gather_code_contents() + "\nautodev.py:\n" + autodev_source
                error_message = stderr if stderr.strip() else stdout
                filename, search_block, replace_block = get_fix_instructions(code_contents, error_message)
                console.print("[blue]Fix instruction generated:[/blue]")
                console.print(f"Filename: {filename}")
                console.print(f"Search block: {search_block}")
                console.print(f"Replace block: {replace_block}")
                if filename is None:
                    console.print("[yellow]No fixer available for this error.[/yellow]")
                else:
                    apply_fix(filename, search_block, replace_block)
            else:
                console.print("[green]autodev.py ran successfully.[/green]")
            console.print("Sleeping for 5 seconds before next check...")
            time.sleep(5)
            if os.path.exists('autodev.py'):
                new_mod_time = os.path.getmtime('autodev.py')
                if new_mod_time != last_mod_time:
                    console.print("[blue]Change detected in autodev.py, re-running pipeline.[/blue]")
                    last_mod_time = new_mod_time

    except KeyboardInterrupt:
        print("Exiting main loop.")

# New function to print the DSPy signature for fix instructions.
# This signature is based on best practices as discussed in [usecodeblocks.com](https://usecodeblocks.com/) and [aider.chat](https://aider.chat/docs/usage.html).

def main():
    helper_function()
    main_loop()

if __name__ == '__main__':
    main()
