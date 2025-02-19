import os
import time
from time import sleep
import pytest
from dspy_pipeline.main_loop import MainLoop

def fake_run_autodev(self):
    # Simulate a NameError in autodev.py
    return (1, "", "NameError: name 'test_function' is not defined")

def fake_sleep(duration):
    raise KeyboardInterrupt

class FakeFixApplier:
    def __init__(self):
        self.applied_fixes = []
    def apply_fix(self, filename, search_block, replace_block):
        self.applied_fixes.append((filename, search_block, replace_block))

def test_main_loop_integration(monkeypatch, tmp_path):
    # Create a dummy autodev.py in the temporary directory
    autodev = tmp_path / "autodev.py"
    autodev.write_text("raise NameError('test_function is not defined')")
    monkeypatch.chdir(tmp_path)

    # Override run_autodev to return a simulated error
    monkeypatch.setattr("dspy_pipeline.autodev_runner.AutodevRunner.run_autodev", fake_run_autodev)
    # Override time.sleep to stop the infinite loop after one iteration
    monkeypatch.setattr(time, "sleep", fake_sleep)
    # Override FixApplier.apply_fix to capture its call parameters
    fake_applier = FakeFixApplier()
    monkeypatch.setattr("dspy_pipeline.fix_applier.FixApplier.apply_fix", fake_applier.apply_fix)

    loop = MainLoop()
    with pytest.raises(KeyboardInterrupt):
        loop.run()

    # According to FixModule NameError branch, fix should be:
    # filename: "autodev.py", search: "test_function()", replacement: "new_test_function()"
    assert fake_applier.applied_fixes, "FixApplier.apply_fix should be called"
    fix = fake_applier.applied_fixes[0]
    assert fix[0] == "autodev.py"
    assert fix[1] == "test_function()"
    assert fix[2] == "new_test_function()"
