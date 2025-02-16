import os
import pytest
from dspy_pipeline.main import get_fix_instructions, apply_fix

def test_get_fix_instructions():
    code_text = "dummy code"
    error_text = "dummy error"
    filename, search_block, replace_block = get_fix_instructions(code_text, error_text)
    # For the dummy fixer, the expected values are:
    assert filename == "autodev.py"
    assert search_block == "foo"
    assert replace_block == "bar"

def test_apply_fix_existing_file(tmp_path):
    # Create a temporary autodev.py file that includes the text "foo"
    file_path = tmp_path / "autodev.py"
    file_path.write_text("this foo is a bug")
    apply_fix(str(file_path), "foo", "bar")
    updated_content = file_path.read_text()
    assert "bar" in updated_content
    assert "foo" not in updated_content

def test_apply_fix_non_existing_file(tmp_path):
    # For a non-existent file, the file should be created with the replace_block
    file_path = tmp_path / "new_autodev.py"
    if file_path.exists():
        file_path.unlink()
    apply_fix(str(file_path), "foo", "bar")
    updated_content = file_path.read_text()
    assert updated_content == "bar"
