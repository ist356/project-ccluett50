import pandas as pd
import json
import os
from needed_functions import american_to_decimal

# Step 1: Read the CSV file
def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        print("CSV file read successfully")
        return df
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

# Step 2: Fix invalid JSON and parse the 'bookmakers' column
def parse_json_column(df, column_name):
    def parse_json(x):
        try:
            return json.loads(x.replace("'", '"'))
        except json.JSONDecodeError as e:
            print(f"JSON decode error for row: {x}\nError: {e}")
            return None

    try:
        df[column_name] = df[column_name].apply(parse_json)
        print("JSON parsing successful")
        return df
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return None

# Step 3: Flatten the bookmakers data
def flatten_data(df):
    flattened_rows = []
    for _, row in df.iterrows():
        if row['bookmakers'] is None:
            continue
        for bookmaker in row['bookmakers']:
            for market in bookmaker['markets']:
                for outcome in market['outcomes']:
                    flattened_rows.append({
                        "id": row["id"],
                        "sport_key": row["sport_key"],
                        "sport_title": row["sport_title"],
                        "commence_time": row["commence_time"],
                        "home_team": row["home_team"],
                        "away_team": row["away_team"],
                        "bookmaker": bookmaker["title"],
                        "market": market["key"],
                        "team": outcome.get("name"),
                        "price": outcome.get("price"),
                        "point": outcome.get("point", None)
                    })

    return pd.DataFrame(flattened_rows)

# Steps 4, 5, 6: Adjust datetime, filter bookmakers, and add decimal odds
def process_and_filter_data(df, bookmakers):
    # Adjust datetime to EST
    df['commence_time'] = pd.to_datetime(df['commence_time'], utc=True)
    df['commence_time'] = df['commence_time'] - pd.Timedelta(hours=5)
    
    # Extract date components
    df['month'] = df['commence_time'].dt.month
    df['day'] = df['commence_time'].dt.day
    df['year'] = df['commence_time'].dt.year
    df['time'] = df['commence_time'].dt.time
    
    # Filter specific bookmakers
    df = df[df['bookmaker'].isin(bookmakers)]
    
    # Add decimal odds conversion
    df['decimal_odds'] = df['price'].apply(american_to_decimal)

    return df

# Step 7: Clean and finalize data
def clean_data(df):
    df['year'] = df['year'].astype(str).str.replace(',', '')
    df['time'] = df['time'].apply(lambda x: x.strftime('%H:%M'))
    df['point'] = df['point'].astype(float).round(1)
    df = df.drop(columns=['sport_key', 'commence_time'])

    return df

# Step 8: Save to CSV
def save_to_csv(df, output_dir, output_file):
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/{output_file}"
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")

# Main function to streamline the process

if __name__ == "__main__":
    input_file = "./cache/combined_odds_american.csv"
    output_dir = "cache"
    output_file = "filtered_odds.csv"
    bookmakers = ["DraftKings", "BetUS", "FanDuel", "BetMGM"]

    # Execute functions in order
    df = read_csv(input_file)
    if df is not None:
        df = parse_json_column(df, 'bookmakers')
        flattened_df = flatten_data(df)
        processed_df = process_and_filter_data(flattened_df, bookmakers)
        final_df = clean_data(processed_df)
        save_to_csv(final_df, output_dir, output_file)
