# utils/api.py
import requests
import pandas as pd
from config import ALPHA_VANTAGE_API_KEY

BASE_URL = "https://www.alphavantage.co/query"

def get_stock_data(symbol, function="TIME_SERIES_DAILY", outputsize="compact"):
    """
    Fetch stock data from Alpha Vantage API.
    """
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
        "outputsize": outputsize
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def get_company_overview(symbol):
    """
    Fetch company overview data from Alpha Vantage API.
    """
    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def get_income_statement(symbol):
    """
    Fetch income statement data from Alpha Vantage API.
    """
    params = {
        "function": "INCOME_STATEMENT",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def get_balance_sheet(symbol):
    """
    Fetch balance sheet data from Alpha Vantage API.
    """
    params = {
        "function": "BALANCE_SHEET",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def get_cash_flow(symbol):
    """
    Fetch cash flow data from Alpha Vantage API.
    """
    params = {
        "function": "CASH_FLOW",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def search_symbol(keywords):
    """
    Search for stock symbols using Alpha Vantage API.
    """
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": keywords,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def process_time_series_data(data):
    """
    Process time series data and return a pandas DataFrame.
    """
    time_series = data.get("Time Series (Daily)")
    if not time_series:
        return None

    df = pd.DataFrame.from_dict(time_series, orient="index")
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)
    df.columns = ["Open", "High", "Low", "Close", "Volume"]
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Date"}, inplace=True)
    return df.sort_index()