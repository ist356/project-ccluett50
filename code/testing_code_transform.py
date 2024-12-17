import pandas as pd
import ast

# Step 1: Read the CSV file
df = pd.read_csv("./cache/combined_odds_american.csv")

# Step 2: Parse the 'bookmakers' column using ast.literal_eval
df['bookmakers'] = df['bookmakers'].apply(ast.literal_eval)

# Step 3: Flatten the data
flattened_rows = []
for _, row in df.iterrows():
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

# Step 4: Convert flattened rows to a DataFrame
flattened_df = pd.DataFrame(flattened_rows)

print(flattened_df)
