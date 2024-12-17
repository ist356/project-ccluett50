import os
import pandas as pd
import pytest

OUTPUT_FILE = "./cache/combined_odds_american.csv"

def test_file_exists_and_not_empty():
    """
    Test to ensure the output file exists and is not empty.
    """
    # Check if the file exists
    assert os.path.exists(OUTPUT_FILE), f"File {OUTPUT_FILE} does not exist!"

    # Check if the file is not empty
    df = pd.read_csv(OUTPUT_FILE)
    assert len(df) > 0, f"File {OUTPUT_FILE} is empty!"

    # Optional: Print debug information if test fails
    print(f"File '{OUTPUT_FILE}' exists and contains {len(df)} rows.")