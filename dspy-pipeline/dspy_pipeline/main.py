import os
import dspy
import logging
from dspy_pipeline.main_loop import MainLoop

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    lm = dspy.LM('openrouter/google/gemini-2.0-flash-001', api_key=os.environ["OPENROUTER_API_KEY"], temperature=1.5, caching=False)
    dspy.configure(lm=lm)
    main_loop = MainLoop()
    main_loop.run()
