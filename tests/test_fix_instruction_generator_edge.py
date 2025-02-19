import pytest
from unittest.mock import patch
from dspy_pipeline.fix_instruction_generator import FixInstructionGenerator
from dspy_pipeline.fix_signature import FixSignature

def test_fix_instruction_generator_lm_failure(caplog):
    # Mock dspy.Predict to raise an exception
    with patch('dspy.Predict.forward') as predict_mock:
        predict_mock.side_effect = Exception("LM failed")

        # Initialize FixInstructionGenerator
        fix_instruction_generator = FixInstructionGenerator()

        # Generate fix instructions
        fix_instructions = fix_instruction_generator.get_fix_instructions("some code", "some error")

        # Assert that an error message was logged
        assert "Error generating fix instructions" in caplog.text

        # Assert that the returned FixSignature contains the error message
        assert "Error generating fix instructions: LM failed" in fix_instructions.replacement
        assert fix_instructions.filename == "UNKNOWN"

def test_fix_instruction_generator_empty_code_error(caplog):
    # Initialize FixInstructionGenerator
    fix_instruction_generator = FixInstructionGenerator()

    # Generate fix instructions with empty code and error
    fix_instructions = fix_instruction_generator.get_fix_instructions("", "")

    # Assert that the returned FixSignature is still valid
    assert isinstance(fix_instructions, FixSignature)

    # Assert that no error message was logged
    assert "Error generating fix instructions" not in caplog.text
