import pytest
from dspy_pipeline.fix_instruction_generator import FixInstructionGenerator

def test_fix_instruction_generator_exception(monkeypatch):
    generator = FixInstructionGenerator()
    # Force predictor to raise an exception
    monkeypatch.setattr(generator, "predictor", lambda code, error: (_ for _ in ()).throw(Exception("Test exception")))
    fix_sig = generator.forward("some code", "error detail")
    assert fix_sig.filename == "UNKNOWN"
    assert fix_sig.search == ""
    assert "# Please add the file content here" in fix_sig.replacement
    assert "Test exception" in fix_sig.replacement
