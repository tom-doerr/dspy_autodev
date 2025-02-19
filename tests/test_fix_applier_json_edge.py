import os
import json
import pytest
from dspy_pipeline.fix_applier import FixApplier

def test_json_patch_on_empty_file(tmp_path, capsys):
    test_file = tmp_path / "ether_module.py"
    test_file.write_text("")
    json_patch = '''[
  {
    "op": "add",
    "path": "/0",
    "value": "def get_ether_price():\\n    return 1000"
  }
]'''
    fix_applier = FixApplier()
    fix_applier.apply_fix(str(test_file), "", json_patch)
    assert test_file.read_text() == ""
    captured = capsys.readouterr().out
    assert "Failed to apply JSON patch" in captured

def test_json_patch_on_non_json_file(tmp_path, capsys):
    test_file = tmp_path / "not_json.py"
    original_content = "def foo():\n    pass\n"
    test_file.write_text(original_content)
    json_patch = '''[
  {
    "op": "add",
    "path": "/0",
    "value": "def get_ether_price():\\n    return 1000"
  }
]'''
    fix_applier = FixApplier()
    fix_applier.apply_fix(str(test_file), "", json_patch)
    assert test_file.read_text() == original_content
    captured = capsys.readouterr().out
    assert "Failed to apply JSON patch" in captured

def test_json_patch_on_valid_json_array(tmp_path):
    test_file = tmp_path / "json_arr.txt"
    test_file.write_text("[]")
    json_patch = '''[
  {
    "op": "add",
    "path": "/0",
    "value": "def get_ether_price():\\n    return 1000"
  }
]'''
    fix_applier = FixApplier()
    fix_applier.apply_fix(str(test_file), "", json_patch)
    new_content = test_file.read_text()
    json_data = json.loads(new_content)
    assert isinstance(json_data, list)
    assert json_data[0] == "def get_ether_price():\n    return 1000"

def test_json_patch_on_valid_json_object(tmp_path):
    test_file = tmp_path / "json_obj.txt"
    test_file.write_text('{"dummy": "value"}')
    json_patch = '''[
  {
    "op": "add",
    "path": "/get_ether_price",
    "value": "def get_ether_price():\\n    return 1000"
  }
]'''
    fix_applier = FixApplier()
    fix_applier.apply_fix(str(test_file), "", json_patch)
    new_content = test_file.read_text()
    json_data = json.loads(new_content)
    assert json_data.get("dummy") == "value"
    assert json_data.get("get_ether_price") == "def get_ether_price():\n    return 1000"
