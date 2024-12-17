import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_functions import display_odds_and_chart, calculate_implied_probability

# Function to calculate implied probability from American odds

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('./cache/filtered_odds.csv')

# Load the data
df = load_data()

# Title
st.title("Sports Betting Odds Viewer")
st.write("Select a sport and view detailed stats for each game!")

# Step 1: Sport Selection
unique_sports = df['sport_title'].unique()
selected_sport = st.selectbox("Choose a sport:", unique_sports)

# Filter games based on sport
sport_games = df[df['sport_title'] == selected_sport]

if sport_games.empty:
    st.write("No games available for this sport.")
else:
    # Step 2: Select a Game
    unique_games = sport_games[['home_team', 'away_team', 'month', 'day', 'year']].drop_duplicates()
    game_options = [
        f"{row['home_team']} vs {row['away_team']} on {row['month']:02}/{row['day']:02}/{row['year']}"
        for _, row in unique_games.iterrows()
    ]
    selected_game = st.selectbox("Choose a game:", game_options)

    # Extract home_team and away_team from selected_game
    game_info = selected_game.split(" on ")[0]
    home_team, away_team = game_info.split(" vs ")

    # Filter data for the selected game
    game_data = sport_games[
        (sport_games['home_team'] == home_team) & (sport_games['away_team'] == away_team)
    ]

    # Display Spread, Total, and H2H Tabs
    bookmakers = ["DraftKings", "BetUS", "FanDuel", "BetMGM"]
    tabs = st.tabs(["Spread Odds", "Total Odds", "H2H Odds"])

    with tabs[0]:
        display_odds_and_chart("spreads")

    with tabs[1]:
        display_odds_and_chart("totals")

    with tabs[2]:
        display_odds_and_chart("h2h")

# Footer
st.write("---")
st.write("Powered by Streamlit")
