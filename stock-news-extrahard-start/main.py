import requests
import datetime
import os
import pandas as pd
from pyexpat.errors import messages
from twilio.rest import Client
import smtplib
import re
from textwrapper import wrap
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


  # I didn't do the sms part of the challenge because twilio returns errors when I try to redeem my trial phone number.
  # The value of the timedelta "day=" parameter must be adjusted to match the days when stocks data is available for otherwise a IndexError error is returned.

today = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(days=4)
day_before_yesterday = today - datetime.timedelta(days=8)

STOCK = "AAPL"
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


def get_news_dataframe():
    response_news = requests.get("https://newsapi.org/v2/everything", params=params_news)
    articles = response_news.json()['articles']
    titles = []
    descriptions = []
    for i in articles:
        # return f'Title: {i['title']} \n\n {i['description']}'
        titles.append([i['title']])
        descriptions.append(i['description'])
    message = pd.DataFrame(descriptions)
    pd.set_option('display.max_colwidth', None)
    return message.encode('utf-8')

def get_news(percentage, string):
    response_news = requests.get("https://newsapi.org/v2/everything", params=params_news)
    articles = response_news.json()['articles']
    message = []
    description_edit = ''
    if os.path.isfile("./file_to_send.txt"):
        print(os.path.isfile("./file_to_send.txt"))
        os.remove("./file_to_send.txt")
    for i in articles:
        with open(file="./file_to_send.txt", mode="a+", encoding='utf-8') as file:  # Mime module to try
            file.writelines(f'{STOCK} {string}{round(percentage, 2)}\n ')
            file.writelines('Title: ')
            # file.writelines(f'{i['title'].encode('ascii', 'replace').decode('utf-8')} \n')  # a solution for parsing
            file.writelines(f'{i['title']} \n')
            file.writelines('Description: ')
            description_edit = i['description']
            try:
                new_description = re.sub('\n\n\n', "", description_edit)
            except TypeError:
                pass
            finally:
                file.writelines(f'{new_description} \n\n')

    # pd.set_option('display.max_colwidth', None)
    # print(pd.DataFrame(message))
    message_edit = ""
    # return '\n'.join(wrap(message, width=25))
    return

def send_email(message):
    sender_email = "szymonbryniakproject@gmail.com"
    receiver_email = "oneplusszymonbryniak@gmail.com"
    subject = "Test Email with Unicode Characters"
    body = message

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=username, password=password)
        connection.sendmail(sender_email, receiver_email, msg.as_string())
print(response.json()['values'])

def check_variance(yesterday_low, day_before_low):
    if yesterday_low > day_before_low:
        print("increase")
        percent = (yesterday_low - day_before_low) / day_before_low * 100
        print(yesterday_low % day_before_low, day_before_low * 0.05)
        if yesterday_low % day_before_low > day_before_low * 0.05 :
            print("News, up by more than 5", day_before_low % yesterday_low, yesterday_low * 0.05)
            print(yesterday_low % day_before_low)
            get_news(percent,"🔺")
            with open('./file_to_send.txt', encoding='utf-8') as file:
                message = file.read()
            send_email(message='Subject: Tesla Stock News\n\n{}'.format(message))
        else:
            get_news(percent,"🔺")
            with open('./file_to_send.txt', encoding='utf-8') as file:
                message = file.read()
            send_email(message='Subject: Tesla Stock News\n\n{}'.format(message))


    elif yesterday_low < day_before_low:
        print("decrease")
        print(day_before_low % yesterday_low, day_before_low * 0.05)
        percent = (yesterday_low - day_before_low) / day_before_low * 100
        if day_before_low % yesterday_low > day_before_low * 0.05:
            print(day_before_low % yesterday_low)
            print("News, down by more than 5")
            get_news(percent,"🔻")
            with open('./file_to_send.txt', encoding='utf-8') as file:
                message = file.read()
            send_email(message='Subject: Tesla Stock News\n\n{}'.format(message))
        else:
            get_news(percent,"🔻")
            with open('./file_to_send.txt', encoding='utf-8') as file:
                message = file.read()
            send_email(message='Subject: Tesla Stock News\n\n{}'.format(message))


# unpack_api(values_list)
check_variance(low_yes, low_day_before_yes)
unpack_api(values_list)
# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
def send_sms():  # unable to get the phone number from twilio ad the time of writing
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Join Earth's mightiest heroes. Like Kevin Bacon.",
        from_="+15017122661",
        to="+15558675310",
    )

    print(message.body)

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

