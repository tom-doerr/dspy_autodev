import dspy

class FixSignature(dspy.Signature):
    """
    Signature for the FixModule, which generates fix instructions based on code and error traceback.
    """
    code_text: str = dspy.InputField(desc="The complete source code of the project.")
    error_text: str = dspy.InputField(desc="The error message or traceback from running the code.")
    filename: str = dspy.OutputField(desc="The name of the file to modify.")
    search: str = dspy.OutputField(desc="The code block to search for in the file.")
    replacement: str = dspy.OutputField(desc="The code block to replace the search block with.")
