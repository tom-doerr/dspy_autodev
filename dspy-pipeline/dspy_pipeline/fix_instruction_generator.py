import logging
import dspy
from dspy.signatures import Signature
from dspy_pipeline.fix_module import FixModule, UNKNOWN_FILE, MISSING_CONTENT_COMMENT, NEW_FILE_COMMENT
from dspy_pipeline.fix_signature import FixSignature

class ErrorToFix(Signature):
    """
    Given code and an error traceback, generate a JSON Patch (in standard JSON Patch format) that fixes the error.
    """
    code: str = dspy.InputField(desc="Combined source code from all files, including autodev.py.")
    error: str = dspy.InputField(desc="Error message and traceback from autodev.py execution.")
    filename: str = dspy.OutputField(desc="File path to apply the fix or create if it does not exist.")
    search: str = dspy.OutputField(desc="Code block to search for (empty if creating a new file).")
    replacement: str = dspy.OutputField(desc="JSON Patch to apply to the code to fix the error.")

class FixInstructionGenerator(dspy.Module):
    def __init__(self, model=None):
        super().__init__()
        self.model = model
        self.predictor = dspy.ChainOfThought(ErrorToFix)

    def forward(self, code: str, error: str) -> FixSignature:
        """
        Generates fix instructions using a DSPy Predict module.
        """
        try:
            try:
                 prediction = self.predictor(code=code, error=error)
            except AssertionError as e:
                 if "No LM is loaded" in str(e):
                      from dspy_pipeline.fix_signature import FixSignature
                      prediction = FixSignature()
                 else:
                      raise
            return prediction

        except Exception as e:
            logging.exception(f"Error generating fix instructions: {e}")
            return FixSignature(
                code_text=code,
                error_text=error,
                filename=UNKNOWN_FILE,
                search="",
                replacement=f"{MISSING_CONTENT_COMMENT}\n# Error generating fix instructions: {e}"
            )

    def get_fix_instructions(self, code: str, error: str) -> FixSignature:
        return self.forward(code, error)
