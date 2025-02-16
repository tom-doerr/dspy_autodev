import pytest
from dspy_pipeline.fix_module import FixModule

def test_fix_module_for_old_function():
    fix_module = FixModule()
    code_text = "def some_code():\n    old_function()\n"
    error_text = (
        "Traceback (most recent call last):\n"
        "  File \"autodev.py\", line 2, in <module>\n"
        "NameError: name 'old_function' is not defined"
    )
    fix = fix_module.forward(code_text, error_text)
    assert fix["filename"] == "autodev.py"
    assert fix["search"] == "old_function()"
    assert fix["replace"] == "new_function()"

def test_fix_module_no_fix():
    # This test ensures that if the error does not match any recognized pattern,
    # the fixer returns fallback instructions that signal manual intervention.
    # Specifically, instead of automatically fixing code, the fixer returns:
    #   - filename: "unknown.py"
    #   - an empty search block
    #   - a placeholder replace block ("# Please add the file content here")
    # This ensures safe modifications aligned with best practices as outlined in
    # [usecodeblocks.com](https://usecodeblocks.com/) and [pep8.org](https://pep8.org/).
    fix_module = FixModule()
    code_text = "def some_code():\n    some_function()\n"
    error_text = (
        "Traceback (most recent call last):\n"
        "  File \"autodev.py\", line 2, in <module>\n"
        "NameError: name 'some_function' is not defined"
    )
    fix = fix_module.forward(code_text, error_text)
    assert fix["filename"] == "unknown.py"
    assert fix["search"] == ""
    assert fix["replace"] == "# Please add the file content here"
