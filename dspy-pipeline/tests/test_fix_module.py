import pytest
import os
from dspy_pipeline.fix_module import FixModule
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
    assert fix.filename == "autodev.py"
    assert fix.search == "old_function()"
    assert fix.replacement == "new_old_function()"

def test_fix_module_file_not_found():
    fix_module = FixModule()
    code_text = "def some_code():\n    import ether_module\n"
    error_text = (
        "Traceback (most recent call last):\n"
        "  File \"autodev.py\", line 1, in <module>\n"
        "ModuleNotFoundError: No module named 'ether_module'"
    )
    fix = fix_module.forward(code_text, error_text)
    assert fix.filename == "unknown.py"
    assert fix.search == ""
    assert fix.replacement == "# New file created by autodev-pipeline\n"

def test_fix_module_no_fix():
    fix_module = FixModule()
    code_text = "def some_code():\n    some_function()\n"
    error_text = (
        "Traceback (most recent call last):\n"
        "  File \"autodev.py\", line 2, in <module>\n"
        "ValueError: invalid literal for int() with base 10: 'some_function'"
    )
    fix = fix_module.forward(code_text, error_text)
    assert fix.filename == "unknown.py"
    assert fix.search == ""
    assert fix.replacement == "# Please add the file content here"

def test_fix_module_other_error():
    fix_module = FixModule()
    code_text = "def some_code(a,b):\n    return a / b\n"
    error_text = (
        "Traceback (most recent call last):\n"
        "  File \"autodev.py\", line 2, in <module>\n"
        "ZeroDivisionError: division by zero"
    )
    fix = fix_module.forward(code_text, error_text)
    assert fix.filename == "unknown.py"
    assert fix.search == ""
    assert fix.replacement == "# Please add the file content here"

def test_fix_applier_file_exists_and_modified(tmpdir):
    file_path = tmpdir.join("test_file.py")
    file_path.write("def some_code():\n    old_function()\n")
    apply_fix(str(file_path), "old_function()", "new_old_function()")
    content = file_path.read()
    assert "new_old_function()" in content
    assert "old_function()" not in content

def test_fix_applier_file_exists_and_modified_windows_line_endings(tmpdir):
    file_path = tmpdir.join("test_file.py")
    file_path.write("def some_code():\r\n    old_function()\r\n")
    apply_fix(str(file_path), "old_function()", "new_old_function()")
    content = file_path.read()
    assert "new_old_function()" in content
    assert "old_function()" not in content.strip()

def test_fix_applier_file_exists_but_search_block_not_found(tmpdir):
    file_path = tmpdir.join("test_file.py")
    file_path.write("def some_code():\n    another_function()\n")
    apply_fix(str(file_path), "old_function()", "new_old_function()")
    content = file_path.read()
    assert "old_function()" not in content
    assert "new_old_function()" not in content
    assert "another_function()" in content

def test_fix_applier_file_does_not_exist(tmpdir):
    file_path = tmpdir.join("new_file.py")
    apply_fix(str(file_path), "", "# New file content")
    assert file_path.read() == "# New file content"

def test_fix_applier_skips_autodev_py(tmpdir):
    file_path = tmpdir.join("autodev.py")
    file_path.write("def some_code():\n    old_function()\n")
    apply_fix(str(file_path), "old_function()", "new_old_function()")
    content = file_path.read()
    assert "old_function()" in content
    assert "new_old_function()" not in content

def test_fix_applier_multiple_occurrences(tmpdir):
    file_path = tmpdir.join("test_file.py")
    file_path.write("def some_code():\n    old_function()\n    old_function()\n")
    apply_fix(str(file_path), "old_function()", "new_old_function()")
    content = file_path.read()
    assert content.count("new_old_function()") == 1
    assert content.count("old_function()") == 1

def test_fix_applier_leading_whitespace(tmpdir):
    file_path = tmpdir.join("test_file.py")
    file_path.write("def some_code():\n    old_function()\n")
    apply_fix(str(file_path), "   old_function()", "new_old_function()")
    content = file_path.read()
    assert "old_function()" in content
    assert "new_old_function()" not in content

def test_fix_applier_trailing_whitespace(tmpdir):
    file_path = tmpdir.join("test_file.py")
    file_path.write("def some_code():\n    old_function()\n")
    apply_fix(str(file_path), "old_function()   ", "new_old_function()")
    content = file_path.read()
    assert "old_function()" in content
    assert "new_old_function()" not in content

def test_fix_applier_empty_file(tmpdir):
    file_path = tmpdir.join("test_file.py")
    file_path.write("")
    apply_fix(str(file_path), "old_function()", "new_old_function()")
    content = file_path.read()
    assert content == ""

# --- Edge Case Tests ---

def test_fix_module_empty_code_text():
    fix_module = FixModule()
    code_text = ""
    error_text = "NameError: name 'old_function' is not defined"
    fix = fix_module.forward(code_text, error_text)
    assert fix.filename == "unknown.py"
    assert fix.search == ""
    assert fix.replacement == "# Please add the file content here"

def test_fix_module_empty_error_text():
    fix_module = FixModule()
    code_text = "def some_code():\n    old_function()\n"
    error_text = ""
    fix = fix_module.forward(code_text, error_text)
    assert fix.filename == "unknown.py"
    assert fix.search == ""
    assert fix.replacement == "# Please add the file content here"
