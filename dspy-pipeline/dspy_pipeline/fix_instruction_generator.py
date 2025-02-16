from dspy_pipeline.fix_module import FixModule

class FixInstructionGenerator:
    def get_fix_instructions(self, code_text: str, error_text: str):
        fix_module = FixModule()
        fix_result = fix_module.forward(code_text, error_text)
        return fix_result.filename, fix_result.search, fix_result.replacement
