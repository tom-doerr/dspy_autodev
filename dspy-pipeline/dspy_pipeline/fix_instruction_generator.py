import logging
import dspy
import logging
import dspy
import logging
import dspy
from dspy.signatures import Signature
from dspy_pipeline.fix_signature import FixSignature

class ErrorToFix(Signature):
    """
    Given code and an error traceback, generate replacement text that fixes the error.
    """
    code: str = dspy.InputField(desc="Combined source code from all files, including autodev.py.")
    error: str = dspy.InputField(desc="Error message and traceback from autodev.py execution.")
    filename: str = dspy.OutputField(desc="File path to apply the fix or create if it does not exist.")
    search: str = dspy.OutputField(desc="Code block to search for (empty if creating a new file).")
    replacement: str = dspy.OutputField(desc="Replacement code or initial file content.")

class FixInstructionGenerator(dspy.Module):
    def __init__(self, model=None):
        super().__init__()
        self.model = model
        self.predictor = dspy.Predict(ErrorToFix)

    def forward(self, code: str, error: str) -> FixSignature:
        """
        Generates fix instructions using a DSPy Predict module.
        """
        try:
            prediction = self.predictor(code=code, error=error)
            return prediction
        except Exception as e:
            logging.exception(f"Error generating fix instructions: {e}")
            return FixSignature(
                code_text=code,
                error_text=error,
                filename="UNKNOWN",
                search="",
                replacement=f"# Error generating fix instructions: {e}"
            )

    def get_fix_instructions(self, code: str, error: str) -> FixSignature:
        return self.forward(code, error)
