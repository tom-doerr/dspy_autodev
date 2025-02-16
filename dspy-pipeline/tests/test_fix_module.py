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
    fix_module = FixModule()
    code_text = "def some_code():\n    some_function()\n"
    error_text = (
        "Traceback (most recent call last):\n"
        "  File \"autodev.py\", line 2, in <module>\n"
        "NameError: name 'some_function' is not defined"
    )
    fix = fix_module.forward(code_text, error_text)
    assert fix["filename"] is None
    assert fix["search"] == ""
    assert fix["replace"] == ""
