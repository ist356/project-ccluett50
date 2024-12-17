import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def calculate_implied_probability(price):
    if price > 0:
        decimal_odds = (price / 100) + 1
    else:
        decimal_odds = (100 / abs(price)) + 1
    return round((1 / decimal_odds) * 100, 1)

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