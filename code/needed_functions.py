def american_to_decimal(american_odds):
        if american_odds > 0:
            return round((american_odds / 100) + 1, 2)
        else:
            return round((100 / abs(american_odds)) + 1, 2)
        
def calculate_implied_probability(price):
    if price > 0:
        decimal_odds = (price / 100) + 1
    else:
        decimal_odds = (100 / abs(price)) + 1
    return round((1 / decimal_odds) * 100, 1)

