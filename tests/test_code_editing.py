import pytest
from dspy_pipeline.fix_applier import FixApplier

def test_apply_fix_replacement(tmpdir):
    # Create a file with known content containing a search block.
    file_path = tmpdir.join("sample.py")
    file_path.write("def func():\n    print('old_content')\n")
    
    fix_applier = FixApplier()
    search_block = "print('old_content')"
    replace_block = "print('new_content')"
    
    # Apply the fix.
    fix_applier.apply_fix(str(file_path), search_block, replace_block)
    
    # Verify that the old content was replaced.
    expected = "def func():\n    print('new_content')\n"
    assert file_path.read() == expected

def test_apply_fix_create_new_file(tmpdir):
    # Define a file path that does not exist.
    new_file = tmpdir.join("new_file.py")
    
    fix_applier = FixApplier()
    # An empty search block indicates that the entire content should be replaced/created.
    fix_applier.apply_fix(str(new_file), "", "print('file created')")
    
    # Assert that the file was created with the expected content.
    assert new_file.check(), "New file should be created"
    assert new_file.read() == "print('file created')"
