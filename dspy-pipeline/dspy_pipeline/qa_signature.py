from dspy import Signature, InputField, OutputField

class BasicQA(Signature):
    """
    A DSPy signature for basic question answering.
    
    Defines a simple QA module that takes a question and returns a short, factoid answer.
    For more details, see [dspy-docs.vercel.app](https://dspy-docs.vercel.app/docs/building-blocks/signatures).
    """
    question = InputField(desc="The question to answer")
    answer = OutputField(desc="A brief factoid answer")
