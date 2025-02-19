import os
import json
import jsonpatch
import pytest
from dspy_pipeline.fix_applier import FixApplier

def test_json_patch_success(tmp_path):
    # Create a valid JSON file with some initial content.
    test_file = tmp_path / "test.json"
    original_data = {"dummy": "value"}
    test_file.write_text(json.dumps(original_data))
    
    # Define a valid JSON patch that adds a new key "newKey" with value "newValue".
    patch = '[{"op": "add", "path": "/newKey", "value": "newValue"}]'
    
    # Instantiate FixApplier and invoke apply_fix to apply the JSON patch.
    fix_applier = FixApplier()
    # Pass an empty search block to trigger the JSON patch branch.
    fix_applier.apply_fix(str(test_file), "", patch)
    
    # Verify that the JSON patch was applied correctly.
    updated_data = json.loads(test_file.read_text())
    assert updated_data.get("dummy") == "value"
    assert updated_data.get("newKey") == "newValue"

def test_json_patch_failure(tmp_path, capsys):
    # Create a file with non-JSON content.
    test_file = tmp_path / "not_json.txt"
    original_content = "This is not JSON content."
    test_file.write_text(original_content)
    
    # Define a JSON patch (this should fail because the file content is not valid JSON).
    patch = '[{"op": "add", "path": "/newKey", "value": "newValue"}]'
    
    # Instantiate FixApplier and attempt to apply the JSON patch.
    fix_applier = FixApplier()
    fix_applier.apply_fix(str(test_file), "", patch)
    
    # Check that the file content remains unchanged because the patch application failed.
    assert test_file.read_text() == original_content
    
    # Optionally, capture console output to verify the expected failure message is printed.
    captured = capsys.readouterr().out
    assert "Failed to apply JSON patch" in captured
