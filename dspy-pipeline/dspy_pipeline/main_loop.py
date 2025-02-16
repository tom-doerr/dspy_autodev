import os
import time
from rich.console import Console
from dspy_pipeline.autodev_runner import AutodevRunner
from dspy_pipeline.code_gatherer import CodeGatherer
from dspy_pipeline.fix_instruction_generator import FixInstructionGenerator
from dspy_pipeline.fix_applier import FixApplier

console = Console()

class MainLoop:
    def __init__(self):
        self.autodev_runner = AutodevRunner()
        self.code_gatherer = CodeGatherer()
        self.fix_instruction_generator = FixInstructionGenerator()
        self.fix_applier = FixApplier()

    def run(self):
        last_mod_time = os.path.getmtime('autodev.py') if os.path.exists('autodev.py') else 0
        try:
            while True:
                retcode, stdout, stderr = self.autodev_runner.run_autodev()
                if retcode != 0 or stderr.strip():
                    console.print("[red]Error encountered while running autodev.py[/red]")
                    console.print("[yellow]Error details:[/yellow]")
                    console.print(stderr if stderr.strip() else stdout)
                    try:
                        with open('autodev.py', 'r', encoding='utf8') as f:
                            autodev_source = f.read()
                    except Exception as e:
                        autodev_source = "Could not read autodev.py: " + str(e)
                    code_contents = self.code_gatherer.gather_code_contents() + "\nautodev.py:\n" + autodev_source
                    error_message = stderr if stderr.strip() else stdout
                    filename, search_block, replace_block = self.fix_instruction_generator.get_fix_instructions(code_contents, error_message)
                    console.print("[blue]Fix instruction generated:[/blue]")
                    console.print(f"Filename: {filename}")
                    console.print(f"Search block: {search_block}")
                    console.print(f"Replace block: {replace_block}")
                    fix_reasoning = "Plan: The error indicates that module 'ether_module' is missing. Consider adding the required module or adjusting the import accordingly."
                    console.print(f"[blue]Reasoning: {fix_reasoning}[/blue]")
                    if filename is None:
                        console.print("[yellow]No fixer available for this error.[/yellow]")
                    else:
                        self.fix_applier.apply_fix(filename, search_block, replace_block)
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
