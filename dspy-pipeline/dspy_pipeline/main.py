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
    # Use dspy.LM to generate fix instructions using model openrouter/google/gemini-2.0-flash-001.
    from dspy import LM
    lm = LM(model="openrouter/google/gemini-2.0-flash-001")
    prompt = (
        "Given the following code, error message, and error traceback, generate fix instructions in the format:\n"
        "Filename: <filename>\n"
        "<<<<<<< SEARCH\n"
        "<search block>\n"
        "=======\n"
        "<replace block>\n"
        ">>>>>>> REPLACE\n\n"
        "Ensure that your fix accounts for the full context and refers to best practices as outlined in the DSPy Cheatsheet [dspy.ai](https://dspy.ai/cheatsheet/) and additional guidelines from [dspy-docs.vercel.app](https://dspy-docs.vercel.app/api/category/modules).\n\n"
        "The code input includes the complete source of autodev.py, preceded by the marker 'autodev.py:'.\n"
        "Code:\n" + code_text + "\n\nError Traceback:\n" + error_text + "\n"
    )
    fix_response = lm.generate(prompt)
    # For demonstration purposes, parse a dummy response.
    # The response must contain the expected format.
    lines = fix_response.splitlines()
    filename = None
    search_block = ""
    replace_block = ""
    for i, line in enumerate(lines):
        if line.startswith("Filename:"):
            filename = line.split(":", 1)[1].strip()
        if line.strip() == "<<<<<<< SEARCH":
            j = i + 1
            search_lines = []
            while j < len(lines) and lines[j].strip() != "=======":
                search_lines.append(lines[j])
                j += 1
            search_block = "\n".join(search_lines)
        if line.strip() == "=======":
            j = i + 1
            replace_lines = []
            while j < len(lines) and lines[j].strip() != ">>>>>>> REPLACE":
                replace_lines.append(lines[j])
                j += 1
            replace_block = "\n".join(replace_lines)
    if filename is None:
        return None, None, None
    return filename, search_block, replace_block

def apply_fix(filename, search_block, replace_block):
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
                print("Error encountered, running fixer.")
                try:
                    with open('autodev.py', 'r', encoding='utf8') as f:
                        autodev_source = f.read()
                except Exception as e:
                    autodev_source = "Could not read autodev.py: " + str(e)
                code_contents = gather_code_contents() + "\nautodev.py:\n" + autodev_source
                error_message = stderr if stderr.strip() else stdout
                filename, search_block, replace_block = get_fix_instructions(code_contents, error_message)
                if filename is None:
                    console.print("[yellow]No fixer available for this error. Sleeping for 5 seconds...[/yellow]")
                else:
                    apply_fix(filename, search_block, replace_block)
                time.sleep(5)
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

# New function to print the DSPy signature for fix instructions.
# This signature is based on best practices as discussed in [usecodeblocks.com](https://usecodeblocks.com/) and [aider.chat](https://aider.chat/docs/usage.html).
def print_dspy_signature():
    signature = (
        "Given the following code, error message, and error traceback, generate fix instructions in the format:\n"
        "Filename: <filename>\n"
        "<<<<<<< SEARCH\n"
        "<search block>\n"
        "=======\n"
        "<replace block>\n"
        ">>>>>>> REPLACE\n\n"
        "Ensure that the patch addresses both the error details and its traceback. Refer to the DSPy Cheatsheet [dspy.ai](https://dspy.ai/cheatsheet/) for common usage patterns and best practices.\n\n"
        "Code:\n"
        "... (truncated for brevity)\n"
    )
    print(signature)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--signature":
        print_dspy_signature()
        sys.exit(0)
    helper_function()
    main_loop()

if __name__ == '__main__':
    main()
