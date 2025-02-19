# Objective

This project aims to build a robust, autonomous error-fixing system that can run any Python program(e.g., autodev.py) without modifying its core files, e.g. autodev.py, since it is used to guide the generation of the rest of the code, to show what the goal is. Instead, the system intelligently analyzes runtime errors—such as missing modules, undefined functions, or other common issues—and dynamically generates the required code to resolve them. By capturing error messages, generating fix instructions with an LLM model, and applying fixes through auxiliary components, the system can iteratively achieve a stable execution state.


