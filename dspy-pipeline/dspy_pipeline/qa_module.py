from dspy_pipeline.qa_signature import BasicQA
from dspy import Predict

class BasicQAModule(Predict):
    """
    A DSPy module for basic question answering built on the BasicQA signature.
    
    This module wraps an LM call to generate answers for input questions.
    In this dummy implementation, it returns a canned answer.
    See [dspy-docs.vercel.app](https://dspy-docs.vercel.app/docs/building-blocks/modules) for details.
    """
    # Associate the signature with this module.
    signature = BasicQA

    def forward(self, question):
        # In a real implementation, you would call your LM here.
        # For demonstration, we return a fixed answer.
        return self.signature.construct(question=question, answer="42")
