import logging
import dspy
from dspy.signatures import Signature
from dspy_pipeline.fix_module import FixModule, UNKNOWN_FILE, MISSING_CONTENT_COMMENT, NEW_FILE_COMMENT
from dspy_pipeline.fix_signature import FixSignature

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') # REMOVE THIS LINE

def generate_fix_instructions(code_text: str, error_text: str) -> FixSignature:
    """
    Generates fix instructions (filename, search string, replacement string) based on the code and error.
    """
    fix_module = FixModule()
    fix_signature = fix_module.forward(code_text, error_text)
    return fix_signature

class ErrorToFix(Signature):
    """
    Given code and an error traceback, generate a fix.
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
            # Use the DSPy Predict module to generate fix instructions
            prediction = self.predictor(code=code, error=error)
            return FixSignature(filename=prediction.filename, search=prediction.search, replacement=prediction.replacement)

        except Exception as e:
            logging.exception(f"Error generating fix instructions: {e}")
            return FixSignature(filename=UNKNOWN_FILE, search="", replacement=f"{MISSING_CONTENT_COMMENT}\n# Error generating fix instructions: {e}")
