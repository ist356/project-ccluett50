from project_code._0_needed_functions import american_to_decimal, calculate_implied_probability
import pytest
test_cases_american = [
    {'american_odds': 200, 'expected': 3.0},
    {'american_odds': -200, 'expected': 1.5},
    {'american_odds': 300, 'expected': 4.0},
    {'american_odds': -500, 'expected': 1.2},
    {'american_odds': 100, 'expected': 2.0},
    {'american_odds': 150, 'expected': 2.5},
    {'american_odds': -150, 'expected': 1.67},
]

# Test function with debug prints
def test_american_to_decimal():
    for test_case in test_cases_american:
        assert american_to_decimal(test_case['american_odds']) == test_case['expected']

test_cases_prob = [{'price': 200, 'expected': 33.3},
                {'price': -200, 'expected': 66.7},
                {'price': 300, 'expected': 25.0},
                {'price': -500, 'expected': 83.3},
                {'price': 100, 'expected': 50.0},
                {'price': -100, 'expected': 50.0},
                {'price': 150, 'expected': 40.0},
                {'price': -150, 'expected': 60.0}]
def test_calculate_implied_probability():
    for test_case in test_cases_prob:
        assert calculate_implied_probability(test_case['price']) == test_case['expected']

