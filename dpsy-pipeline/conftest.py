import sys
import os

# Add the dpsy-pipeline folder to sys.path.
# This ensures that the dpsy_pipeline package is discoverable.
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
