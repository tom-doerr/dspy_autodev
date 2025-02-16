import subprocess
from rich.console import Console

console = Console()

class AutodevRunner:
    def run_autodev(self):
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

    def get_autodev_source(self):
        """
        Reads the contents of autodev.py and returns it as a string.
        """
        try:
            with open("autodev.py", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "autodev.py not found."
        except Exception as e:
            return f"Error reading autodev.py: {e}"
