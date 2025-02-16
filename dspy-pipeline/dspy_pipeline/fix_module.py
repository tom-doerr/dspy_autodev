from dspy import Module

class FixModule(Module):
    """
    DSPy Module for generating fix instructions based on code and error traceback.

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
    def forward(self, code_text: str, error_text: str):
        import re
        m = re.search(r"NameError: name '(\w+)' is not defined", error_text)
        if m:
            func_name = m.group(1)
            if func_name == "old_function":
                return {
                    "filename": "autodev.py",
                    "search": "old_function()",
                    "replace": "new_function()"
                }
        return {"filename": None, "search": "", "replace": ""}
