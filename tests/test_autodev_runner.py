import pytest
import os
from dspy_pipeline.autodev_runner import AutodevRunner

def test_autodev_runner_success(tmpdir, monkeypatch):
    # Create a dummy autodev.py file
    autodev_file = tmpdir.join("autodev.py")
    autodev_file.write("print('Success!')")

    # Change the current working directory to the temporary directory
    monkeypatch.chdir(tmpdir)

    # Initialize AutodevRunner
    runner = AutodevRunner()

    # Run autodev.py
    retcode, stdout, stderr = runner.run_autodev()

    # Assert that the return code is 0
    assert retcode == 0

    # Assert that the stdout contains "Success!"
    assert "Success!" in stdout

    # Assert that the stderr is empty
    assert stderr == ""

def test_autodev_runner_failure(tmpdir, monkeypatch):
    # Create a dummy autodev.py file that raises an exception
    autodev_file = tmpdir.join("autodev.py")
    autodev_file.write("raise Exception('Failure!')")

    # Change the current working directory to the temporary directory
    monkeypatch.chdir(tmpdir)

    # Initialize AutodevRunner
    runner = AutodevRunner()

    # Run autodev.py
    retcode, stdout, stderr = runner.run_autodev()

    # Assert that the return code is not 0
    assert retcode != 0

    # Assert that the stderr contains "Exception: Failure!"
    assert "Exception: Failure!" in stderr

    # Assert that the stdout is empty
    assert stdout == ""

def test_autodev_runner_get_autodev_source(tmpdir, monkeypatch):
    # Create a dummy autodev.py file
    autodev_file = tmpdir.join("autodev.py")
    autodev_file.write("print('Success!')")

    # Change the current working directory to the temporary directory
    monkeypatch.chdir(tmpdir)

    # Initialize AutodevRunner
    runner = AutodevRunner()

    # Get the source code of autodev.py
    source_code = runner.get_autodev_source()

    # Assert that the source code is correct
    assert source_code == "print('Success!')"

def test_autodev_runner_get_autodev_source_file_not_found(tmpdir, monkeypatch):
    # Change the current working directory to the temporary directory
    monkeypatch.chdir(tmpdir)
    
    # Initialize AutodevRunner
    runner = AutodevRunner()
    
    # Get the source code of autodev.py
    source_code = runner.get_autodev_source()
    
    # Assert that the source code is correct
    assert source_code == "autodev.py not found."

def test_autodev_runner_mixed_output(tmpdir, monkeypatch):
    # Create a dummy autodev.py that prints both stdout and stderr.
    # This test follows best-practices from [stackoverflow.com](https://stackoverflow.com/questions/44629510/using-pytest-to-ensure-a-file-is-created-and-written-to)
    # and addresses handling discussed in [github.com](https://github.com/paul-gauthier/aider/issues/82).
    autodev_file = tmpdir.join("autodev.py")
    autodev_file.write("import sys\nprint('Partial success')\nprint('Warning: something happened', file=sys.stderr)\n")
    
    monkeypatch.chdir(tmpdir)
    runner = AutodevRunner()
    retcode, stdout, stderr = runner.run_autodev()
    
    # Check that the return code is 0 because the script did not raise an exception
    assert retcode == 0
    # Ensure stdout contains "Partial success"
    assert "Partial success" in stdout
    # Ensure stderr contains the warning message
    assert "Warning: something happened" in stderr
