import os
import sys

# Ensure `samples/app` (the directory containing main.py) is importable
# regardless of where pytest is invoked from.
HERE = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(HERE)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)
