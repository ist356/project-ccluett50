import requests
import pandas as pd
import os

def fetch_odds(sport, params, headers) -> pd.DataFrame:
    """
    Fetch odds data from the Odds API and save it to a CSV file.

    Parameters:
        api_key (str): Your API key for Odds API.
        sport (str): Sport key, e.g., 'americanfootball_nfl'.
        regions (str): Comma-separated regions, e.g., 'us,uk,eu'.
        markets (str): Comma-separated markets, e.g., 'h2h,spreads,totals'.
        output_dir (str): Directory to save the fetched data.
    """
    # Base URL for the Odds API
    BASE_URL = "https://api.the-odds-api.com/v4/sports"

    # Define headers and parameters for the API request
    

    

    # Build the full API URL dynamically
    url = f"{BASE_URL}/{sport}/odds/"

    # Make the API request

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    df = pd.json_normalize(data)

    return df



if __name__ == "__main__":
    # Step 1: Open sports_matches.csv
    sports_matches_df = pd.read_csv("./cache/sports_matches.csv")
    
    # Step 2: Filter for titles matching "NCAAB", "NFL", "NCAAF", "NBA", "NHL"
    desired_titles = ["NCAAB", "NFL", "NCAAF", "NBA", "NHL"]
    filtered_df = sports_matches_df[sports_matches_df['title'].isin(desired_titles)]
    
    # Step 3: Extract 'key' values into a list
    sports = filtered_df['key'].tolist()
    print(f"Sports keys to fetch odds: {sports}")

    # Step 4: Set API parameters
    params = {
        #"apiKey": "8d53f6317401301f0e6d342ab72fba59",
        "regions": "us",
        "markets": "h2h,spreads,totals",
        "oddsFormat": "american"
    }

    headers = {
        "Content-Type": "application/json"
    }

    # Step 5: Fetch odds for each sport and append DataFrames together
    all_odds_df = pd.DataFrame()

    for sport in sports:
        print(f"Fetching odds for: {sport}")
        odds_df = fetch_odds(sport, params, headers)
        if not odds_df.empty:
            all_odds_df = pd.concat([all_odds_df, odds_df], ignore_index=True)

    # Step 6: Save the combined DataFrame to a CSV file
    output_dir = "cache"
    os.makedirs(output_dir, exist_ok=True)
    combined_file_path = os.path.join(output_dir, "combined_odds_american.csv")
    all_odds_df.to_csv(combined_file_path, index=False)

    print(f"Combined odds data saved to: {combined_file_path}")
