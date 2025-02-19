import os
from dspy_pipeline.fix_applier import FixApplier

def test_apply_fix_success(tmpdir, caplog):
    # Create a dummy file
    file1 = tmpdir.join("file1.py")
    file1.write("def hello():\n    print('Hello, world!')\n")

    # Initialize FixApplier
    applier = FixApplier()

    # Define the filename, search block, and replace block
    filename = str(file1)
    search_block = "print('Hello, world!')"
    replace_block = "print('Hello, world! fixed')"

    # Apply the fix
    applier.apply_fix(filename, search_block, replace_block)

    # Assert that the file content has been updated
    assert file1.read() == "def hello():\n    print('Hello, world! fixed')\n"
