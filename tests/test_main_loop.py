import pytest
from unittest.mock import MagicMock
from dspy_pipeline.main_loop import MainLoop
from dspy_pipeline.fix_signature import FixSignature


def test_main_loop_run_success():
    # Create mock objects for the dependencies
    autodev_runner_mock = MagicMock()
    code_gatherer_mock = MagicMock()
    fix_instruction_generator_mock = MagicMock()
    fix_applier_mock = MagicMock()

    # Configure the mock objects
    autodev_runner_mock.run_autodev.return_value = (0, "Success!", "")
    autodev_runner_mock.get_autodev_source.return_value = "print('Success!')"
    code_gatherer_mock.gather_code.return_value = ({}, [])
    fix_instruction_generator_mock.forward.return_value = FixSignature(filename="test.py", search="old_code", replacement="new_code", code_text="code", error_text="error")

    # Create a MainLoop instance with the mock objects
    main_loop = MainLoop()
    main_loop.autodev_runner = autodev_runner_mock
    main_loop.code_gatherer = code_gatherer_mock
    main_loop.fix_instruction_generator = fix_instruction_generator_mock
    main_loop.fix_applier = fix_applier_mock

    # Run the main loop for 1 iteration
    main_loop.run(iterations=1)

    # Assert that the mock objects were called correctly
    autodev_runner_mock.run_autodev.assert_called_once()
    autodev_runner_mock.get_autodev_source.assert_called_once()
    code_gatherer_mock.gather_code.assert_called_once()
    fix_instruction_generator_mock.forward.assert_called_once()
    fix_applier_mock.apply_fix.assert_called_once_with("test.py", "old_code", "new_code")


def test_main_loop_run_failure():
    # Create mock objects for the dependencies
    autodev_runner_mock = MagicMock()
    code_gatherer_mock = MagicMock()
    fix_instruction_generator_mock = MagicMock()
    fix_applier_mock = MagicMock()

    # Configure the mock objects
    autodev_runner_mock.run_autodev.return_value = (1, "", "Failure!")
    autodev_runner_mock.get_autodev_source.return_value = "raise Exception('Failure!')"
    code_gatherer_mock.gather_code.return_value = ({}, [])
    fix_instruction_generator_mock.forward.return_value = FixSignature(filename="test.py", search="old_code", replacement="new_code", code_text="code", error_text="error")

    # Create a MainLoop instance with the mock objects
    main_loop = MainLoop()
    main_loop.autodev_runner = autodev_runner_mock
    main_loop.code_gatherer = code_gatherer_mock
    main_loop.fix_instruction_generator = fix_instruction_generator_mock
    main_loop.fix_applier = fix_applier_mock

    # Run the main loop for 1 iteration
    main_loop.run(iterations=1)

    # Assert that the mock objects were called correctly
    autodev_runner_mock.run_autodev.assert_called_once()
    autodev_runner_mock.get_autodev_source.assert_called_once()
    code_gatherer_mock.gather_code.assert_called_once()
    fix_instruction_generator_mock.forward.assert_called_once()
    fix_applier_mock.apply_fix.assert_called_once_with("test.py", "old_code", "new_code")
