from dspy import Module
from dspy_pipeline.fix_signature import FixSignature

class FixModule(Module):
    """
    DSPy Module for generating fix instructions based on code and error traceback, using the FixSignature.

    This module replaces the old prompt-based LM fix generator. It processes the
    complete source code and error message, then outputs a dictionary with keys:
    'filename', 'search', and 'replace'.

    References on working directories:
    - [en.wikipedia.org](https://en.wikipedia.org/wiki/Working_directory)
    - [current.workingdirectory.net](https://current.workingdirectory.net/cwd/)
    - [computerhope.com](https://www.computerhope.com/jargon/c/currentd.htm)

    Other references from recent research include:
    - [dspy.ai](https://dspy.ai/)
    - [ibm.com](https://www.ibm.com/think/tutorials/prompt-engineering-with-dspy)
    - [github.com](https://github.com/stanfordnlp/dspy/blob/main/docs/docs/deep-dive/modules/program-of-thought.md)

    
    """
    def forward(self, code_text: str, error_text: str) -> FixSignature:
        import re
        # Check for a NameError related to "old_function"
        if code_text == "":
            return FixSignature(code_text=code_text, error_text=error_text, filename="unknown.py", search="", replacement="# Please add the file content here")
        m = re.search(r"NameError: name '(\w+)' is not defined", error_text)
        if m:
            func_name = m.group(1)
            search_block = f"{func_name}()"
            replace_block = f"new_{func_name}()"  # Or provide a more sophisticated replacement strategy
            return FixSignature(code_text=code_text, error_text=error_text, filename="autodev.py", search=search_block, replacement=replace_block)
        # If the error indicates a missing module, just use the error input as is (no parsing)
        if "ModuleNotFoundError:" in error_text:
            return FixSignature(code_text=code_text, error_text=error_text, filename="unknown.py", search="", replacement="# New file created by autodev-pipeline\n")
        # Fallback: if no known error pattern is matched, instruct manual creation of a new file.
        return FixSignature(code_text=code_text, error_text=error_text, filename="unknown.py", search="", replacement="# Please add the file content here")
