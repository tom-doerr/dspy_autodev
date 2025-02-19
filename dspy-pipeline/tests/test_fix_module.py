import pytest
import re
import os
from dspy_pipeline.fix_module import FixModule, UNKNOWN_FILE, AUTODEV_FILE, NEW_FILE_COMMENT, MISSING_CONTENT_COMMENT
from dspy_pipeline.fix_applier import FixApplier

apply_fix = FixApplier().apply_fix

# --- FixModule Tests ---

def test_fix_module_name_error():
    fix_module = FixModule()
    code_text = "def some_code():\n    old_function()\n"
    error_text = (
        "Traceback (most recent call last):\n"
        "  File \"autodev.py\", line 2, in <module>\n"
        "NameError: name 'old_function' is not defined"
    )
    fix = fix_module.forward(code_text, error_text)
    assert fix.filename == AUTODEV_FILE, "Filename should be autodev.py"
    assert fix.search == "old_function()", "Search string should match the missing function call"
    assert fix.replacement == "new_old_function()", "Replacement should suggest a new function name"

def test_fix_module_file_not_found():
    fix_module = FixModule()
    code_text = "def some_code():\n    import ether_module\n"
    error_text = (
        "Traceback (most recent call last):\n"
        "  File \"autodev.py\", line 1, in <module>\n"
        "ModuleNotFoundError: No module named 'ether_module'"
    )
    fix = fix_module.forward(code_text, error_text)
    assert fix.filename == "ether_module.py", "Filename should be the missing module name"
    assert fix.search == "", "Search string should be empty for new file creation"
    assert fix.replacement == NEW_FILE_COMMENT, "Replacement should indicate new file creation"

def test_fix_module_no_fix():
    fix_module = FixModule()
    code_text = "def some_code():\n    some_function()\n"
    error_text = (
        "Traceback (most recent call last):\n"
        "  File \"autodev.py\", line 2, in <module>\n"
        "ValueError: invalid literal for int() with base 10: 'some_function'"
    )
    fix = fix_module.forward(code_text, error_text)
    assert fix.filename == UNKNOWN_FILE, "Filename should be unknown.py for unhandled errors"
    assert fix.search == "", "Search string should be empty for unhandled errors"
    assert fix.replacement == f"{MISSING_CONTENT_COMMENT}\n# Original error: Traceback (most recent call last):\n  File \"autodev.py\", line 2, in <module>\nValueError: invalid literal for int() with base 10: 'some_function'", "Replacement should instruct manual creation and include the original error"

def test_fix_module_other_error():
    fix_module = FixModule()
    code_text = "def some_code(a,b):\n    return a / b\n"
    error_text = (
        "Traceback (most recent call last):\n"
        "  File \"autodev.py\", line 2, in <module>\n"
        "ZeroDivisionError: division by zero"
    )
    fix = fix_module.forward(code_text, error_text)
    assert fix.filename == UNKNOWN_FILE, "Filename should be unknown.py for unhandled errors"
    assert fix.search == "", "Search string should be empty for unhandled errors"
    assert fix.replacement == f"{MISSING_CONTENT_COMMENT}\n# Original error: Traceback (most recent call last):\n  File \"autodev.py\", line 2, in <module>\nZeroDivisionError: division by zero", "Replacement should instruct manual creation and include the original error"

def test_fix_applier_file_exists_and_modified(tmpdir):
    file_path = tmpdir.join("test_file.py")
    file_path.write("def some_code():\n    old_function()\n")
    apply_fix(str(file_path), "old_function()", "new_old_function()")
    content = file_path.read()
    assert re.search(r"\bnew_old_function\(\)\b", content), "The replacement should be in the file"
    assert not re.search(r"\bold_function\(\)\b", content), "The original code should not be in the file"

def test_fix_applier_file_exists_and_modified_windows_line_endings(tmpdir):
    file_path = tmpdir.join("test_file.py")
    file_path.write("def some_code():\r\n    old_function()\r\n")
    apply_fix(str(file_path), "old_function()", "new_old_function()")
    content = file_path.read()
    assert re.search(r"\bnew_old_function\(\)\b", content), "The replacement should be in the file"
    assert not re.search(r"\bold_function\(\)\b", content), "The original code should not be in the file"

def test_fix_applier_file_exists_but_search_block_not_found(tmpdir):
    file_path = tmpdir.join("test_file.py")
    file_path.write("def some_code():\n    another_function()\n")
    apply_fix(str(file_path), "old_function()", "new_old_function()")
    content = file_path.read()
    assert "old_function()" not in content, "The original code should not be in the file"
    assert "new_old_function()" not in content, "The replacement should not be in the file"
    assert "another_function()" in content, "The existing code should still be in the file"

def test_fix_applier_file_does_not_exist(tmpdir):
    file_path = tmpdir.join("new_file.py")
    apply_fix(str(file_path), "", "# New file content")
    assert file_path.read() == "# New file content", "The file should be created with the new content"

def test_fix_applier_skips_autodev_py(tmpdir):
    file_path = tmpdir.join("autodev.py")
    file_path.write("def some_code():\n    old_function()\n")
    apply_fix(str(file_path), "old_function()", "new_old_function()")
    content = file_path.read()
    assert "old_function()" in content, "The original code should still be in the file"
    assert "new_old_function()" not in content, "The replacement should not be in the file"

def test_fix_applier_multiple_occurrences(tmpdir):
    file_path = tmpdir.join("test_file.py")
    file_path.write("def some_code():\n    old_function()\n    old_function()\n")
    apply_fix(str(file_path), "old_function()", "new_old_function()")
    content = file_path.read()
    assert len(re.findall(r"\bnew_old_function\(\)\b", content)) == 1, "The replacement should only occur once"
    assert len(re.findall(r"\bold_function\(\)\b", content)) == 1, "One original code occurrence should remain"

def test_fix_applier_leading_whitespace(tmpdir):
    file_path = tmpdir.join("test_file.py")
    file_path.write("def some_code():\n    old_function()\n")
    apply_fix(str(file_path), "   old_function()", "new_old_function()")
    content = file_path.read()
    assert not re.search(r"\bold_function\(\)\b", content), "The original code should not be in the file"
    assert re.search(r"\bnew_old_function\(\)\b", content), "The replacement should be in the file"

def test_fix_applier_trailing_whitespace(tmpdir):
    file_path = tmpdir.join("test_file.py")
    file_path.write("def some_code():\n    old_function()\n")
    apply_fix(str(file_path), "old_function()   ", "new_old_function()")
    content = file_path.read()
    assert not re.search(r"\bold_function\(\)\b", content), "The original code should not be in the file"
    assert re.search(r"\bnew_old_function\(\)\b", content), "The replacement should be in the file"

def test_fix_applier_empty_file(tmpdir):
    file_path = tmpdir.join("test_file.py")
    file_path.write("")
    apply_fix(str(file_path), "old_function()", "new_old_function()")
    content = file_path.read()
    assert content == "", "The file should remain empty"

# --- Edge Case Tests ---

def test_fix_module_empty_code_text():
    fix_module = FixModule()
    code_text = ""
    error_text = "NameError: name 'old_function' is not defined"
    fix = fix_module.forward(code_text, error_text)
    assert fix.filename == UNKNOWN_FILE, "Filename should be unknown.py for empty code"
    assert fix.search == "", "Search string should be empty for empty code"
    assert fix.replacement == MISSING_CONTENT_COMMENT, "Replacement should instruct manual creation for empty code"

def test_fix_module_empty_error_text():
    fix_module = FixModule()
    code_text = "def some_code():\n    old_function()\n"
    error_text = ""
    fix = fix_module.forward(code_text, error_text)
    assert fix.filename == UNKNOWN_FILE, "Filename should be unknown.py for empty error"
    assert fix.search == "", "Search string should be empty for empty error"
    assert fix.replacement == f"{MISSING_CONTENT_COMMENT}\n# Original error: ", "Replacement should instruct manual creation and include the original error"

def test_fix_module_type_error():
    fix_module = FixModule()
    code_text = "def some_code():\n    return 1 + '1'\n"
    error_text = "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
    fix = fix_module.forward(code_text, error_text)
    assert fix.filename == UNKNOWN_FILE, "Filename should be unknown.py for TypeError"
    assert fix.search == "", "Search string should be empty for TypeError"
    assert fix.replacement == f"# TypeError: Review the types being used. Original error: TypeError: unsupported operand type(s) for +: 'int' and 'str'", "Replacement should indicate type error and include the original error"
