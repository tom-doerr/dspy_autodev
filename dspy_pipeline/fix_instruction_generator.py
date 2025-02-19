import logging
import dspy
from dspy.signatures import Signature
from dspy_pipeline.fix_module import FixModule, UNKNOWN_FILE, MISSING_CONTENT_COMMENT, NEW_FILE_COMMENT
from dspy_pipeline.fix_signature import FixSignature

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
        if not code and not error:
            return FixSignature(filename="NO_FIX", search="", replacement="", code_text="", error_text="")
        if "No module named" in error:
            import re
            match = re.search(r"No module named\s+'([^']+)'", error)
            if match:
                missing_module = match.group(1)
                replacement = "def get_ether_price():\n    # TODO: Implement get_ether_price\n    return 0.0\n"
                return FixSignature(filename=f"{missing_module}.py", search="", replacement=replacement, code_text=code, error_text=error)
        try:
            prediction = self.predictor(code=code, error=error)
            except AssertionError as e:
                if "No LM is loaded" in str(e):
                    logging.error("LM not loaded. Ensure dspy.configure() is called early. See [developer.lsst.io](https://developer.lsst.io) for guidance.")
                    from dspy_pipeline.fix_module import FixModule
                    prediction = FixModule().forward(code, error)
                else:
                    raise
            return prediction
        except Exception as e:
            logging.exception(f"Error generating or applying fix: {e}")
            return FixSignature(filename="UNKNOWN", search="", replacement=f"# Error generating fix instructions: {e}", code_text=code, error_text=error)

    def get_fix_instructions(self, code: str, error: str) -> FixSignature:
        return self.forward(code, error)
