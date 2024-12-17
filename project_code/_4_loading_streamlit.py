import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from project_code._0_needed_functions import calculate_implied_probability

# Function to display odds and charts
def display_odds_and_chart(market):
    cols = st.columns(4)  # Creates 4 equal columns
    implied_probabilities = []

    # Define paths to logos
    LOGOS = {
        "DraftKings": "./cache/images/DraftKings_logo.png",
        "BetUS": "./cache/images/BetUS.png",
        "FanDuel": "./cache/images/fanduelLogo.png",
        "BetMGM": "./cache/images/BetMgm.png"
    }

    # Collect implied probabilities and display odds with point data
    for i, bookmaker in enumerate(bookmakers):
        bookmaker_data = game_data[(game_data['bookmaker'] == bookmaker) & (game_data['market'] == market)]
        if not bookmaker_data.empty:
            with cols[i]:
                st.write(f"### {bookmaker}")  # Display bookmaker name

                # Display metrics
                for _, row in bookmaker_data.iterrows():
                    team = row['team']
                    price = row['price']
                    point = row.get('point', None)  # Fetch point data
                    implied_prob = calculate_implied_probability(price)

                    implied_probabilities.append({
                        "team": team,
                        "bookmaker": bookmaker,
                        "implied_prob": implied_prob
                    })

                    # Display odds, exclude point for H2H market
                    if market == "h2h":
                        team_display = f"**{team}**"
                    else:
                        team_display = f"**{team} ({point})**" if point else f"**{team}**"

                    st.markdown(f"{team_display}<br><span style='font-size: 1.2em;'>{price}</span>", 
                                unsafe_allow_html=True)

                # Display logo after metrics
                st.image(LOGOS[bookmaker], width=80)

    # Visualization Section
    if implied_probabilities:
        prob_df = pd.DataFrame(implied_probabilities)

        # Calculate team averages
        avg_team_probs = prob_df.groupby('team')['implied_prob'].mean().reset_index()

        st.write("### Implied Probability Chart")
        fig, ax = plt.subplots()

        # Plot implied probabilities
        for bookmaker in bookmakers:
            bookmaker_data = prob_df[prob_df['bookmaker'] == bookmaker]
            ax.bar(bookmaker_data['team'] + f" ({bookmaker})", 
                   bookmaker_data['implied_prob'], label=bookmaker)

        # Team-only average lines
        for _, row in avg_team_probs.iterrows():
            ax.axhline(row['implied_prob'], color='gray', linestyle='--', 
                       label=f"Avg {row['team']}: {row['implied_prob']:.1f}%")

        # Set y-axis limits based on market
        if market in ['spreads', 'totals']:
            ax.set_ylim(40, 60)  # Set y-axis limits for Spread and Totals

        ax.set_ylabel("Implied Probability (%)")
        ax.set_xlabel("Teams by Bookmaker")
        ax.legend()
        plt.xticks(rotation=45, ha='right')

        st.pyplot(fig)


# Load data
#@st.cache_data
#def load_data():
   # return pd.read_csv('./cache/filtered_odds.csv')

# Load the data
#df = load_data()

df = pd.read_csv('./cache/filtered_odds.csv')

# Title
st.title("Sports Betting Odds APP")
st.write("Select a Sport & Game and Compare the Odds from Different Bookmakers!")

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
    tabs = st.tabs(["Moneyline","Spread Odds", "Over/Under" ])

    with tabs[0]:
        display_odds_and_chart("h2h")

    with tabs[1]:
        display_odds_and_chart("spreads")

    with tabs[2]:
        display_odds_and_chart("totals")

