import pandas as pd
import json

# Step 1: Read the CSV file

df = pd.read_csv("./cache/combined_odds_american.csv")
print("CSV file read successfully")


# Step 2: Fix invalid JSON and parse the 'bookmakers' column
def parse_json(x):
    try:
        return json.loads(x.replace("'", '"'))
    except json.JSONDecodeError as e:
        print(f"JSON decode error for row: {x}\nError: {e}")
        return None

try:
    df['bookmakers'] = df['bookmakers'].apply(parse_json)
    print("JSON parsing successful")
except Exception as e:
    print(f"Error parsing JSON: {e}")

# Step 3: Flatten the data
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
print("Data flattening successful")

# Step 4: Convert flattened rows to a DataFrame

flattened_df = pd.DataFrame(flattened_rows)
print("DataFrame creation successful")

flattened_df = pd.DataFrame(flattened_rows)

# Step 5: Fix datetime format
flattened_df['commence_time'] = pd.to_datetime(flattened_df['commence_time'], utc=True)

flattened_df['commence_time'] = flattened_df['commence_time'] - pd.Timedelta(hours=5)


flattened_df['month'] = flattened_df['commence_time'].dt.month
flattened_df['day'] = flattened_df['commence_time'].dt.day
flattened_df['year'] = flattened_df['commence_time'].dt.year
flattened_df['time'] = flattened_df['commence_time'].dt.time

# Step 6: Filter bookmakers
bookmakers = ["DraftKings", "BetUS", "FanDuel", "BetMGM"]
filtered_df = flattened_df[flattened_df['bookmaker'].isin(bookmakers)]

# Step 7: Drop unnecessary columns
filtered_df = filtered_df.drop(columns=['sport_key', 'commence_time'])
filtered_df['year'] = filtered_df['year'].astype(str).str.replace(',', '')
filtered_df['time'] = filtered_df['time'].apply(lambda x: x.strftime('%H:%M'))

# Display results
print("List of unique bookmakers:")
print(filtered_df['bookmaker'].unique())
print("\nFiltered DataFrame:")
print(filtered_df)

# create a new column for decimal odds and convert the odds to decimal from american odds
def american_to_decimal(american_odds):
    if american_odds > 0:
        return round((american_odds / 100) + 1, 2)
    else:
        return round((100 / abs(american_odds)) + 1, 2)
    
filtered_df['decimal_odds'] = filtered_df['price'].apply(american_to_decimal)

#make sure the spreads are float to 1 decimal if not empty
filtered_df['point'] = filtered_df['point'].astype(float).round(1)

# Step 8: Save the DataFrame to a CSV file
output_dir = "cache"
output_file = "filtered_odds.csv"
output_path = f"{output_dir}/{output_file}"
filtered_df.to_csv(output_path, index=False)