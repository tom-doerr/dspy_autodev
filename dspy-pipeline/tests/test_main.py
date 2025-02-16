import os
import pytest
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dspy_pipeline.fix_instruction_generator import FixInstructionGenerator
from dspy_pipeline.fix_applier import FixApplier
