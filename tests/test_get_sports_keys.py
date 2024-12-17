from project_code._1_api_get_sports_key import get_sports

def test_get_sports():
    API_KEY = "" #put API KEY Here
    BASE_URL = "https://api.the-odds-api.com/v4"
    df = get_sports(API_KEY=API_KEY, BASE_URL=BASE_URL)
    assert len(df) == 55
