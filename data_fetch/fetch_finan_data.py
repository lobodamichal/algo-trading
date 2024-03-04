import yfinance as yf
import pandas as pd
import datetime as dt

def historic_data(name, tickers, days):
    end_date = dt.date.today()
    start_date = pd.to_datetime(end_date) - pd.Timedelta(days=days)
    
    data_df = yf.download(tickers, start=start_date, end=end_date).stack(future_stack=True)

    data_df.index.names = ['date', 'ticker']
    data_df.columns = data_df.columns.str.lower()

    data_df.to_excel(f'../data/historical_{name}_{days}days.xlsx')

    return data_df