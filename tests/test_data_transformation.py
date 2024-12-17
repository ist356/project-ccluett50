import pytest
import pandas as pd
import os
import json
from project_code._0_needed_functions import american_to_decimal
from project_code._3_transform_data import (
    read_csv,
    parse_json_column,
    flatten_data,
    process_and_filter_data,
    clean_data
)

# Mock Data for Testing
MOCK_CSV_PATH = "./cache/mock_combined_odds_american.csv"
OUTPUT_DIR = "./cache"
OUTPUT_FILE = "mock_filtered_odds.csv"

@pytest.fixture
def mock_data():
    """
    Provide a mock DataFrame simulating combined_odds_american.csv.
    """
    data = {
        "id": ["1"],
        "sport_key": ["americanfootball_nfl"],
        "sport_title": ["NFL"],
        "commence_time": ["2024-12-18T02:00:00Z"],
        "home_team": ["Team A"],
        "away_team": ["Team B"],
        "bookmakers": [json.dumps([{
            "title": "DraftKings",
            "markets": [
                {"key": "h2h", "outcomes": [{"name": "Team A", "price": -200}, {"name": "Team B", "price": 150}]},
                {"key": "spreads", "outcomes": [{"name": "Team A", "price": -110, "point": -3.5}]}
            ]
        }])]
    }
    df = pd.DataFrame(data)
    df.to_csv(MOCK_CSV_PATH, index=False)
    yield df
    os.remove(MOCK_CSV_PATH)

# Test: Read CSV
def test_read_csv(mock_data):
    df = read_csv(MOCK_CSV_PATH)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "bookmakers" in df.columns

# Test: Parse JSON Column
def test_parse_json_column(mock_data):
    df = read_csv(MOCK_CSV_PATH)
    df = parse_json_column(df, "bookmakers")
    assert isinstance(df['bookmakers'].iloc[0], list)  # Check JSON loaded successfully
    assert "markets" in df['bookmakers'][0][0]

# Test: Flatten Data
def test_flatten_data(mock_data):
    df = read_csv(MOCK_CSV_PATH)
    df = parse_json_column(df, "bookmakers")
    flattened_df = flatten_data(df)
    assert not flattened_df.empty
    assert "bookmaker" in flattened_df.columns
    assert "market" in flattened_df.columns
    assert "price" in flattened_df.columns

# Test: Process and Filter Data
def test_process_and_filter_data(mock_data):
    df = read_csv(MOCK_CSV_PATH)
    df = parse_json_column(df, "bookmakers")
    flattened_df = flatten_data(df)
    bookmakers = ["DraftKings", "FanDuel"]
    processed_df = process_and_filter_data(flattened_df, bookmakers)
    assert not processed_df.empty
    assert "decimal_odds" in processed_df.columns
    assert "bookmaker" in processed_df.columns
    assert processed_df['bookmaker'].iloc[0] in bookmakers

# Test: Clean Data
def test_clean_data(mock_data):
    df = read_csv(MOCK_CSV_PATH)
    df = parse_json_column(df, "bookmakers")
    flattened_df = flatten_data(df)
    bookmakers = ["DraftKings"]
    processed_df = process_and_filter_data(flattened_df, bookmakers)
    cleaned_df = clean_data(processed_df)
    assert not cleaned_df.empty
    assert "year" in cleaned_df.columns
    assert "month" in cleaned_df.columns
    assert "time" in cleaned_df.columns
    assert "sport_key" not in cleaned_df.columns

# Test End-to-End Process
def test_end_to_end(mock_data):
    df = read_csv(MOCK_CSV_PATH)
    if df is not None:
        df = parse_json_column(df, 'bookmakers')
        flattened_df = flatten_data(df)
        processed_df = process_and_filter_data(flattened_df, ["DraftKings"])
        final_df = clean_data(processed_df)

        # Save to a temporary file
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
        final_df.to_csv(output_path, index=False)

        # Check if file exists and has content
        assert os.path.exists(output_path), "Output file not created!"
        assert os.path.getsize(output_path) > 0, "Output file is empty!"
        os.remove(output_path)
