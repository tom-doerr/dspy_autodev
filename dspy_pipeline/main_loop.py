from dspy_pipeline.code_gatherer import CodeGatherer  # Add this import

class MainLoop:
    def __init__(self):
        self.autodev_runner = AutodevRunner()
        self.code_gatherer = CodeGatherer() # Instantiate CodeGatherer
        self.fix_instruction_generator = FixInstructionGenerator()

    def run(self):
        # ... other code ...
        code_data = self.code_gatherer.gather_code()
        # Now you can work with the code_data dictionary, which contains file paths and code.
        # ... more code ...
