"""
builds the OUTPUT_ files from INPUT/. Run with: python run_merger.py
(Replaces running NEWUSPORTSDataMerger.py.)
"""

import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from merger.pipeline import main

if __name__ == "__main__":
    main()
