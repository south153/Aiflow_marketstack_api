import requests
import os
from datetime import date
import csv
import pandas as pd


# I am aware this is ridiculously over-engineered
# these are your input variables change these to match your portfolio
my_portfolio = ("MSFT", "BRKB", "TAN", "FSLR", "VOO","GME")
shares_owned = [1, 2, 3, 4, 5,12]

# these are all constants
TODAY = date.today()
TODAYS_DATE = TODAY.strftime("%b-%d-%Y")
STOCKS_LIST = []
API_KEY = os.environ.get('STOCK_API_KEY')  # Don't use a config because I'm only using the one secret


def get_stock(stock_ticker):
    """
    Gets the stock data for market stack api and appends symbol and most recent price to list of list
    :param stock_ticker: takes the ticker for any given stock, doesn't work for alot of ETF's
    :return: Does not return any values
    """
    stock_list = stock_ticker
    params = {
        'access_key': API_KEY,
        'symbols': stock_list}
    api_result = requests.get('http://api.marketstack.com/v1/intraday/latest', params)
    api_response = api_result.json()
    for stock_data in api_response['data']:
        STOCKS_LIST.append([TODAYS_DATE, stock_data['symbol'], stock_data['last']])
    print(STOCKS_LIST)

for i in my_portfolio:
    get_stock(i)


# way simpler way of doing this but again over-engineering for fun
# use list comprehension to split so we can multiply the price by how many shares of each stock I own
dates = [sublist[0] for sublist in STOCKS_LIST]
stock_codes = [sublist[1] for sublist in STOCKS_LIST]
price = [STOCKS_LIST[0][2] * shares_owned[i] for i in range(len(shares_owned))]
final_list = []

# put sub-lists back together again
for i in range(len(shares_owned)):
    final_list.append([dates[i], stock_codes[i], price[i]])
print(final_list)




with open('C:\\python_import\\stocks.csv', 'a', newline='') as csvfile:
    data_write = csv.writer(csvfile)
    data_write.writerows(final_list)
print("Write successful {} api calls used".format(len(shares_owned)))
