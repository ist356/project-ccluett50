import os
import pandas as pd

# Ensure the directories exist
output_dir = "cache"
os.makedirs(output_dir, exist_ok=True)

# Read the CSV file
sports_df = pd.read_csv('./cache/sports.csv')

# Create two dataframes based on the 'has_outrights' column
sports_futures_df = sports_df[sports_df['has_outrights'] == True]
sports_matches_df = sports_df[sports_df['has_outrights'] == False]

# Define file paths
futures_file = os.path.join(output_dir, 'sports_futures.csv')
matches_file = os.path.join(output_dir, 'sports_matches.csv')

# Write the dataframes to separate CSV files
sports_futures_df.to_csv(futures_file, index=False)
sports_matches_df.to_csv(matches_file, index=False)

