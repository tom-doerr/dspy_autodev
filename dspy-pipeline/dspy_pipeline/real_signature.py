from dspy import Signature, InputField, OutputField
from typing import Literal

class SentimentAnalysis(Signature):
    """
    DSPy signature for performing sentiment analysis.
    
    This signature analyzes input text and outputs the corresponding sentiment.
    Supported sentiments: "positive", "neutral", "negative".
    
    References:
      - [usecodeblocks.com](https://usecodeblocks.com/)
      - [aider.chat](https://aider.chat)
    """
    text: str = InputField(desc="Input text for sentiment analysis.")
    sentiment: Literal["positive", "neutral", "negative"] = OutputField(desc="Detected sentiment.")
