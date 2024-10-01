import requests
import os
import datetime

yesterday = datetime.date.today() - datetime.timedelta(days=1)
day_before_yesterday = datetime.date.today() - datetime.timedelta(days=15)
today = datetime.date.today()
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
FUNCTION = ""
SYMBOL = STOCK

my_key = os.environ.get("POLYGON_API_KEY")
print(my_key)
params = {
    "interval": "30min",
    "symbol": SYMBOL,
    "type": "stock",
    "end_date": today,
    "format": "JSON",
    "start_date": yesterday,
    "apikey": "f8b725ad9f264f19aa75b5fe93c0f2b3"
}


# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
response = requests.get('https://api.twelvedata.com/time_series', params=params)
response.raise_for_status()
values_list = response.json()['values']
print(yesterday, day_before_yesterday)


def unpack_api(values):
    for i in values:
        print(i)


def check_variance(yesterday_low, day_before_low):
    if yesterday_low % day_before_low > yesterday_low * 0.05:
        print("Get News")
    

unpack_api(values_list)

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

