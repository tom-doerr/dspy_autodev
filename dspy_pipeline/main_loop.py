from dspy_pipeline.code_gatherer import CodeGatherer
from dspy_pipeline.autodev_runner import AutodevRunner  # Add this import
from dspy_pipeline.fix_instruction_generator import FixInstructionGenerator  # Add this import


class MainLoop:
    def __init__(self):
        self.autodev_runner = AutodevRunner()
        self.code_gatherer = CodeGatherer() # Instantiate CodeGatherer
        self.fix_instruction_generator = FixInstructionGenerator()

    def run(self):
        """
        Runs the main loop of the autodev pipeline.
        """
        try:
            # Run autodev.py and capture its output
            autodev_result = self.autodev_runner.run_autodev()
            autodev_source = self.autodev_runner.get_autodev_source()

            # Gather code from the project
            code_data = self.code_gatherer.gather_code()
            code_contents = "\n".join([f"{filepath}:\n{code}" for filepath, code in code_data.items()])

            # Combine code contents and autodev.py source
            combined_code = code_contents + "\nautodev.py:\n" + autodev_source

            # Generate fix instructions from the error and code
            fix_instructions = self.fix_instruction_generator.get_fix_instructions(combined_code, autodev_result.stderr)

            # Print the fix instructions
            print(fix_instructions)

        except Exception as e:
            print(f"An error occurred: {e}")
