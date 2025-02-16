import pytest
import os
from dspy_pipeline.code_gatherer import CodeGatherer

# --- CodeGatherer Tests ---

def test_gather_code_with_python_files(tmpdir):
    # Create some dummy Python files
    file1 = tmpdir.join("file1.py")
    file1.write("def hello():\n    print('Hello, world!')\n")
    file2 = tmpdir.join("file2.py")
    file2.write("def goodbye():\n    print('Goodbye!')\n")
    file3 = tmpdir.join("file3.txt")  # This should be ignored

    # Initialize CodeGatherer with the temporary directory
    gatherer = CodeGatherer(root_dir=str(tmpdir))

    # Gather code with the .py extension
    code_dict, errors = gatherer.gather_code(extensions=(".py",))

    # Assert that the dictionary contains the correct files and content
    assert str(file1) in code_dict
    assert str(file2) in code_dict
    assert str(file3) not in code_dict  # Ensure .txt file is ignored
    assert code_dict[str(file1)] == "def hello():\n    print('Hello, world!')\n"
    assert code_dict[str(file2)] == "def goodbye():\n    print('Goodbye!')\n"
    assert not errors, "No errors should be reported"

def test_gather_code_with_multiple_extensions(tmpdir):
    # Create some dummy files with different extensions
    file1 = tmpdir.join("file1.py")
    file1.write("def hello():\n    print('Hello, world!')\n")
    file2 = tmpdir.join("file2.txt")
    file2.write("Some text content\n")

    # Initialize CodeGatherer with the temporary directory
    gatherer = CodeGatherer(root_dir=str(tmpdir))

    # Gather code with both .py and .txt extensions
    code_dict, errors = gatherer.gather_code(extensions=(".py", ".txt"))

    # Assert that the dictionary contains the correct files and content
    assert str(file1) in code_dict
    assert str(file2) in code_dict
    assert code_dict[str(file1)] == "def hello():\n    print('Hello, world!')\n"
    assert code_dict[str(file2)] == "Some text content\n"
    assert not errors, "No errors should be reported"

def test_gather_code_handles_unreadable_files(tmpdir, caplog):
    # Create a file that cannot be read
    file1 = tmpdir.join("unreadable.py")
    file1.write("def hello():\n    print('Hello, world!')\n")
    os.chmod(str(file1), 0o000)  # Make the file unreadable

    # Initialize CodeGatherer with the temporary directory
    gatherer = CodeGatherer(root_dir=str(tmpdir))

    # Gather code, which should trigger an error log
    code_dict, errors = gatherer.gather_code(extensions=(".py",))

    # Assert that the dictionary is empty (or doesn't contain the unreadable file)
    assert str(file1) not in code_dict

    # Assert that an error message was logged
    assert "Error reading file" in caplog.text

    # Restore permissions to allow cleanup
    os.chmod(str(file1), 0o777)

def test_get_code_for_file_success(tmpdir):
    # Create a dummy file
    file1 = tmpdir.join("file1.py")
    file1.write("def hello():\n    print('Hello, world!')\n")

    # Initialize CodeGatherer with the temporary directory
    gatherer = CodeGatherer(root_dir=str(tmpdir))

    # Get code for the file
    code = gatherer.get_code_for_file(str(file1))

    # Assert that the code is correct
    assert code == "def hello():\n    print('Hello, world!')\n"

def test_get_code_for_file_not_found(tmpdir, caplog):
    # Initialize CodeGatherer with the temporary directory
    gatherer = CodeGatherer(root_dir=str(tmpdir))

    # Try to get code for a non-existent file
    code = gatherer.get_code_for_file(str(tmpdir.join("nonexistent.py")))

    # Assert that the code is None
    assert code is None

    # Assert that an error message was logged
    assert "File not found" in caplog.text

def test_code_gatherer_different_root_dir(tmpdir):
    # Create a subdirectory
    subdir = tmpdir.mkdir("subdir")

    # Create a file inside the subdirectory
    file1 = subdir.join("file1.py")
    file1.write("def hello():\n    print('Hello, world!')\n")

    # Initialize CodeGatherer with the parent directory
    gatherer = CodeGatherer(root_dir=str(tmpdir))

    # Gather code with the .py extension
    code_dict, errors = gatherer.gather_code(extensions=(".py",))

    # The file should NOT be found, as the root dir is the parent
    assert str(file1) not in code_dict
    assert not errors, "No errors should be reported"

    # Initialize CodeGatherer with the subdirectory
    gatherer = CodeGatherer(root_dir=str(subdir))

    # Gather code with the .py extension
    code_dict, errors = gatherer.gather_code(extensions=(".py",))

    # The file SHOULD be found
    assert str(file1) in code_dict
    assert code_dict[str(file1)] == "def hello():\n    print('Hello, world!')\n"
    assert not errors, "No errors should be reported"
