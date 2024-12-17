from project_code._1_api_get_sports_key import get_sports

def test_get_sports():
    API_KEY = "8d53f6317401301f0e6d342ab72fba59"
    BASE_URL = "https://api.the-odds-api.com/v4"
    df = get_sports(API_KEY=API_KEY, BASE_URL=BASE_URL)
    assert len(df) == 55
