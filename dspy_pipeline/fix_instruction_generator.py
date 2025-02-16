import logging
from dspy import Predict
from dspy.signatures import Signature
from dspy_pipeline.fix_module import FixModule, UNKNOWN_FILE, MISSING_CONTENT_COMMENT, NEW_FILE_COMMENT
from dspy_pipeline.fix_signature import FixSignature

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ErrorToFix(Signature):
    """
    Given code and an error traceback, generate a fix.
    """
    code = str
    error = str
    filename = str
    search = str
    replacement = str

class FixInstructionGenerator:
    def __init__(self, model=None):
        self.fix_module = FixModule()
        self.model = model

    def get_fix_instructions(self, code_text: str, error_text: str) -> FixSignature:
        """
        Generates fix instructions (filename, search string, replacement string) based on the code and error.
        """
        try:
            # Use the FixModule to generate fix instructions
            fix_signature = self.fix_module.forward(code_text, error_text)
            return fix_signature

        except Exception as e:
            logging.error(f"Error generating fix instructions: {e}")
            return FixSignature(filename=UNKNOWN_FILE, search="", replacement=f"{MISSING_CONTENT_COMMENT}\n# Error generating fix instructions: {e}")
