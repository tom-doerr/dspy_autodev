import os
import pytest
from dspy_pipeline.main import get_fix_instructions, apply_fix


def test_apply_fix_non_existing_file(tmp_path):
    # For a non-existent file, the file should be created with the replace_block
    file_path = tmp_path / "new_autodev.py"
    if file_path.exists():
        file_path.unlink()
    apply_fix(str(file_path), "foo", "bar")
    updated_content = file_path.read_text()
    assert updated_content == "bar"
