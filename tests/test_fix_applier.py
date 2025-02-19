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

def test_apply_fix_skips_autodev(tmpdir, caplog):
    # Create a dummy autodev.py file
    autodev_file = tmpdir.join("autodev.py")
    autodev_file.write("print('This is autodev.py')")

    # Initialize FixApplier
    applier = FixApplier()

    # Define the filename, search block, and replace block
    filename = str(autodev_file)
    search_block = "print('This is autodev.py')"
    replace_block = "print('This should not be applied')"

    # Apply the fix
    applier.apply_fix(filename, search_block, replace_block)

    # Assert that the file content has not been updated
    assert autodev_file.read() == "print('This is autodev.py')"

    # Assert that a message was logged
    assert "Skipping modification of autodev.py" in caplog.text
