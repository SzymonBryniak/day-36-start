import requests
import datetime
import os
from twilio.rest import Client
import smtplib

yesterday = datetime.date.today() - datetime.timedelta(days=2)
day_before_yesterday = datetime.date.today() - datetime.timedelta(days=2)
today = datetime.date.today()
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
FUNCTION = ""
SYMBOL = STOCK
password = "aruj ltqt spax soaw"
username = "szymonbryniakproject@gmail.com"
to_addrs = "oneplusszymonbryniak@gmail.com"
# my_key = os.environ.get("POLYGON_API_KEY")

params = {
    "interval": "8h",
    "symbol": SYMBOL,
    "type": "stock",
    "end_date": today,
    "format": "JSON",
    "start_date": yesterday,
    "apikey": "f8b725ad9f264f19aa75b5fe93c0f2b3"
}

params_news = {
    "q": SYMBOL,
    "pageSize": 3,
    "from": yesterday,
    "apiKey": "bf0d9b70bac24191a67a0d862d109172"
}

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
response = requests.get('https://api.twelvedata.com/time_series', params=params)
response.raise_for_status()
values_list = response.json()['values']


low_yes = eval(values_list[0]['low'])
low_day_before_yes = eval(values_list[1]['low'])


def unpack_api(values):
    for i in values:
        print(i)


def get_news():
    response_news = requests.get("https://newsapi.org/v2/everything", params=params_news)
    articles = response_news.json()['articles']
    for i in articles:
        print(i)


def check_variance(yesterday_low, day_before_low):
    if yesterday_low > day_before_low:
        if yesterday_low % day_before_low * 0.05:
            print("News, up by more than 5")
            print(yesterday_low % day_before_low)
    elif yesterday_low < day_before_low:
        if day_before_low % yesterday_low * 0.05:
            print(day_before_low % yesterday_low)
            print("News, down by more than 5")
            get_news()


# unpack_api(values_list)
check_variance(low_yes, low_day_before_yes)

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
def send_sms():  # waiting for the phone number from twilio
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Join Earth's mightiest heroes. Like Kevin Bacon.",
        from_="+15017122661",
        to="+15558675310",
    )

    print(message.body)
def send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=username, password=password)
        connection.sendmail(from_addr=username, to_addrs="oneplusszymonbryniak@gmail.com", msg=" test message")
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

send_email()