# TODO

## Action Items

- **Remove KeyboardInterrupt expectation in main loop integration test.**

  Update test in `tests/test_main_loop_integration.py` to not expect a `KeyboardInterrupt` since the main loop no longer raises it.
  
- **Refine regex assertions in fix module tests.**

  Adjust regex patterns in `dspy-pipeline/tests/test_fix_module.py` to account for potential variations in whitespace and formatting.

- **Ensure LM (Language Model) configuration is executed early.**

  Verify that `dspy.configure()` is called before any component (like the fix instruction generator) requires the LM. Consult [docs.python.org](https://docs.python.org/3/library/sys.html) for environment details and [docs.python.org](https://docs.python.org/3/tutorial/interpreter.html) for interpreter behavior.

- **Revisit the fix applier logic.**

  Add logging around file content modifications to determine why expected replacements are not occurring. Use feedback from [docs.python.org](https://docs.python.org/3/tutorial/modules.html) on module design to structure the file modifications.

- **Review test expectations and update tests accordingly.**

  Ensure that all test cases match the latest system behavior and remove outdated expectations (e.g., expecting exceptions that are no longer raised).

## References

- [docs.python.org](https://docs.python.org/3/library/sys.html)
- [docs.python.org](https://docs.python.org/3.8/library/sys.html)
- [docs.python.org](https://docs.python.org/3/tutorial/interpreter.html)
- [docs.python.org](https://docs.python.org/3/tutorial/modules.html)
- [docs.python.org](https://docs.python.org/3.4/library/sys.html)
