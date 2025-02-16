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

def run_autodev():
    result = subprocess.run(
        ['python', 'autodev.py'],
        capture_output=True,
        text=True
    )
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
    # Dummy fixer: replace the first occurrence of "foo" with "bar" in autodev.py.
    filename = "autodev.py"
    search_block = "foo"
    replace_block = "bar"
    return filename, search_block, replace_block

def apply_fix(filename, search_block, replace_block):
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
                print("Error encountered, running fixer.")
                code_contents = gather_code_contents()
                error_message = stderr if stderr.strip() else stdout
                filename, search_block, replace_block = get_fix_instructions(code_contents, error_message)
                apply_fix(filename, search_block, replace_block)
        else:
            print("No errors found.")
        time.sleep(5)
        if os.path.exists('autodev.py'):
            new_mod_time = os.path.getmtime('autodev.py')
            if new_mod_time != last_mod_time:
                print("Change detected in autodev.py, re-running pipeline.")
                last_mod_time = new_mod_time

    except KeyboardInterrupt:
        print("Exiting main loop.")

def main():
    helper_function()
    main_loop()

if __name__ == '__main__':
    main()
