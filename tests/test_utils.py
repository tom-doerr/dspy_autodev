from dspy_pipeline.utils import helper_function

def test_helper_function(capsys):
    # Call the helper function
    helper_function()

    # Capture the output
    captured = capsys.readouterr()

    # Assert that the output is correct
    assert "Helper function from utils." in captured.out
