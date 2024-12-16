import requests
import os
import pandas as pd

# Replace with your API Key
API_KEY = "8d53f6317401301f0e6d342ab72fba59"
BASE_URL = "https://api.the-odds-api.com/v4"

# 1. Fetch all sports
def get_sports():
    ''' 
    Using the API, this fetches all sports the API can gather data on, then it stores the data in a dataframe to be accessed later. This data is important because it has the key needed to call the data
    '''
    url = f"{BASE_URL}/sports/?apiKey={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    df = pd.json_normalize(data)
    new_column_order = ["title", "group", "description", "key", "active", "has_outrights"]
    df = df[new_column_order]
    return df
    

if __name__ == "__main__":
    sports = get_sports()
    print(sports)

    cache_dir = "cache"
    os.makedirs(cache_dir, exist_ok=True)

    # Save the DataFrame to the cache folder
    file_path = os.path.join(cache_dir, "sports.csv")
    sports.to_csv(file_path, index=False)