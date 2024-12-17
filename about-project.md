# About My Project

Student Name:  Connor Cluett
Student Email:  cpcluett@syr.edu

### What it does
So this project is all about Sportsbooks and their changing odds between different online sportsbooks. While most odds are generally very close, some books have -10 or +10 differences while the line is the same, so this project seeks to show the 4 largest mobile sportsbooks, compares their odds so if someone wants to pick a certain line for a certain game they can get the most money for their risk. I found an online API called odds-api (https://the-odds-api.com/), and it has data on upcoming sporting events with the current real time odds by sportbook. It had data for upcoming matches and future bets (Choosing an outright winner for the season such as winning Super Bowl or World Series etc.) I chose just the match data as there are hundreds of events every day and this has the most variability, thus a pipeline would be important to call the data and have it perfectly fit in a web app to show the change in odds. With the match data, I saved as a csv, selected the top 4 sportsbooks as data to keep, and then munged the data so I could use it in an app. I then for every game, through 5 leagues (I just selected leagues that had American games and were playing this time of year, NBA, NCAAF, etc, because there should be odds from the American sportsbooks on these matches) provide the sportsbook spread, over under total, and moneyline (Choosing the team outright). A lot of these terms could be confusing if you do not have prior experience with sportsbetting so I can attach a link if you would like more info --- (https://www.si.com/betting/2022/03/11/sports-betting-101-moneyline-over-under-odds-spreads-terminology). Overall, this API shows which lines are best to bet, so you can switch apps to get as much money as you can for risking the same bet. Overall, this just shows the current odds so you can make more money if you choose to sports bet and gamble responsibly. 

### How you run my project
NOTE*****So because this is an API you need a key, signing up is easy on odds-api.com for 500 requests a month (I only used 62 for my project and could recall it to get more accurate data) or just use my files and API key as I have more requests left over

1. run requirements.txt using terminal -> new terminal -> pip install -r requirements.txt
    this downloads all required imports so you can use them in the code later 

2. run the code files _0_needed_functions.py through _3_transform_data.py in order (by numbers) using just python
    _0_ is some basic functions I made to change the odds into probability and decimal odds from American Odss. Just different formats of data, but very important
    _1_ calls the API the first time to get all of the list of different sports the API can scrape, getting the sports_key needed to run it in _2_ as a param
    _2_ calls the API to get the sports matches that are upcoming the leagues that are playing now and provides the output into a DF that is saved to CSV
    _3_ Munges the data, removing data from Sportsbooks that are smaller, adding datetime columns, removing unimportant columns, etc. saved to a csv that is final for the streamlit

3. Then go to tests and ensure all tests run to then proceed with the last step
    In the test bar that looks like a test beaker, run until all are green checks to show everything is completed correctly

4. Run _4_loading_streamlit.py as a streamlit file using launch.json to run it. You then will be redirected to your browser where you can play around with the different games, select a game you are interested in making a wager on, and find the best odds on what you want to bet.
    This is the streamlit, an Interactive python UI, that has the data, important metrics, and a key visualization

### Other things you need to know
the data should be in a format that is readily called, depending on time of your I would have to change the market codes to include summer American sport markets. Everything should be good if you keep the csv files I downloaded from the API and just run them as your own. I used AI to assist in code and specifically in making the test functions so there should be no errors there. I was having difficulties with the tests at first but they all run perfectly now. 
