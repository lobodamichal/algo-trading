import yfinance as yf
import pandas as pd
import datetime as dt

def historic_data(tickers, years):
    end_date = dt.date.today()
    start_date = pd.to_datetime(end_date) - pd.Timedelta(days=365*years)
    
    data_df = yf.download(tickers, start=start_date, end=end_date).stack(future_stack=True)

    data_df.index.names = ['date', 'ticker']
    data_df.columns = data_df.columns.str.lower()

    return data_df