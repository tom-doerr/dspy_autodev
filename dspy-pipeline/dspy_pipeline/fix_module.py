import re
from dspy import Module
from dspy_pipeline.fix_signature import FixSignature

# Constants for better readability and maintainability
UNKNOWN_FILE = "unknown.py"
AUTODEV_FILE = "autodev.py"
NEW_FILE_COMMENT = "# New file created by autodev-pipeline\n"
MISSING_CONTENT_COMMENT = "# Please add the file content here"

class FixModule(Module):
    """
    DSPy Module for generating fix instructions based on code and error traceback, using the FixSignature.
    """
    def forward(self, code_text: str, error_text: str) -> FixSignature:

        if not code_text:
            return FixSignature(code_text=code_text, error_text=error_text, filename=UNKNOWN_FILE, search="", replacement=MISSING_CONTENT_COMMENT)

        # Check for a NameError related to undefined variables/functions
        name_error_match = re.search(r"NameError: name '(\w+)' is not defined", error_text)
        if name_error_match:
            missing_name = name_error_match.group(1)
            search_block = f"{missing_name}()"  # Naive approach: assumes it's a function call
            replace_block = f"new_{missing_name}()"  # Suggest renaming (very basic)
            return FixSignature(code_text=code_text, error_text=error_text, filename=AUTODEV_FILE, search=search_block, replacement=replace_block)

        # If the error indicates a missing module, create a new file
        module_not_found_match = re.search(r"ModuleNotFoundError: No module named\s+'(\w+)'", error_text)
        if module_not_found_match:
            missing_module = module_not_found_match.group(1)
            return FixSignature(code_text=code_text, error_text=error_text, filename=f"{missing_module}.py", search="", replacement=NEW_FILE_COMMENT)

        # Example: Handling a TypeError (very basic)
        type_error_match = re.search(r"TypeError: unsupported operand type\(s\) for \+", error_text) # Example regex
        if type_error_match:
            return FixSignature(code_text=code_text, error_text=error_text, filename=UNKNOWN_FILE, search="", replacement=f"# TypeError: Review the types being used. Original error: {error_text}")

        # Fallback: if no known error pattern is matched, instruct manual creation of a new file.
        return FixSignature(code_text=code_text, error_text=error_text, filename=UNKNOWN_FILE, search="", replacement=f"{MISSING_CONTENT_COMMENT}\n# Original error: {error_text}")
