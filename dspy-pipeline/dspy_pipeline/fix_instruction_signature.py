from dspy import Signature, InputField, OutputField

class FixInstruction(Signature):
    """
    DSPy signature for generating fix instructions.

    Inputs:
      - code: The complete source code from all relevant files (e.g., autodev.py and others).
      - error: The error message and traceback produced by running autodev.py.

    Outputs:
      - filename: The file path to be fixed or created.
      - search: The code block to search for in the file (empty if creating a new file).
      - replace: The code to replace the search block with (or the initial content if new).
      
    This signature is designed to capture all inputs and outputs for the fix pipeline.
    For more details on multi-field signatures, see [developer.bitcoin.org](https://developer.bitcoin.org/devguide/transactions.html)
    and [docs.solana.com](https://docs.solana.com/developing/programming-model/transactions).
    """
    code: str = InputField(desc="Combined source code from all files, including autodev.py.")
    error: str = InputField(desc="Error message and traceback from autodev.py execution.")
    filename: str = OutputField(desc="File path to apply the fix or create if it does not exist.")
    search: str = OutputField(desc="Code block to search for (empty if creating a new file).")
    replace: str = OutputField(desc="Replacement code or initial file content.")
