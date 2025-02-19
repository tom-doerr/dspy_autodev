import pytest
import os
from dspy_pipeline.main_loop import MainLoop
from dspy_pipeline.autodev_runner import AutodevRunner
from dspy_pipeline.code_gatherer import CodeGatherer
from dspy_pipeline.fix_instruction_generator import FixInstructionGenerator
from dspy_pipeline.fix_applier import FixApplier

def test_main_loop_integration(tmpdir, monkeypatch, caplog):
    # Create a dummy autodev.py that produces an ImportError
    autodev_file = tmpdir.join("autodev.py")
    autodev_file.write("from ether_module import get_ether_price\nprint(get_ether_price())")

    # Change the current working directory to the temporary directory
    monkeypatch.chdir(tmpdir)

    # Create a MainLoop instance
    main_loop = MainLoop()

    # Run the main loop for 1 iteration
    main_loop.run(iterations=1)

    # Assert that ether_module.py was created and contains the expected code
    ether_module_file = tmpdir.join("ether_module.py")
    assert ether_module_file.exists()
    assert "def get_ether_price():" in ether_module_file.read()
    assert "return 1000.0" in ether_module_file.read()

    # Assert that no JSON was written to ether_module.py
    assert ether_module_file.read().startswith("def ")

    # Assert that the correct log messages were generated
    assert "Applied fix to ether_module.py" in caplog.text

def test_main_loop_integration_autodev_modified(tmpdir, monkeypatch, caplog):
    # Create a dummy autodev.py
    autodev_file = tmpdir.join("autodev.py")
    autodev_file.write("print('Initial autodev code')")

    # Change the current working directory to the temporary directory
    monkeypatch.chdir(tmpdir)

    # Create a MainLoop instance
    main_loop = MainLoop()

    # Run the main loop for 1 iteration
    main_loop.run(iterations=1)

    # Assert that autodev.py was not modified
    assert "print('Initial autodev code')" in autodev_file.read()

def test_main_loop_integration_syntax_error(tmpdir, monkeypatch, caplog):
    # Create a dummy autodev.py with a syntax error
    autodev_file = tmpdir.join("autodev.py")
    autodev_file.write("print('Syntax error')\nprint(unterminated string)")

    # Change the current working directory to the temporary directory
    monkeypatch.chdir(tmpdir)

    # Create a MainLoop instance
    main_loop = MainLoop()

    # Run the main loop for 1 iteration
    main_loop.run(iterations=1)

    # Assert that an error message was logged
    assert "Error generating or applying fix" in caplog.text
