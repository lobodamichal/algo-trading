import datetime as dt
import pandas as pd
import yfinance as yf

class Index():
    def __init__(self, name: str):
        self.name = name
        self.tickers = []
        self.gics: pd.DataFrame
        self.financial_data: pd.DataFrame

    def fetch_tickers(self, url) -> None:
        tickers_df = pd.read_html(url)[0]
        tickers_df['Symbol'] = tickers_df['Symbol'].str.replace('.', '-')

        self.gics = tickers_df
        self.tickers = tickers_df['Symbol'].unique().tolist()

    def fetch_financial_data(self, days=None) -> None:
        end_date = dt.date.today()

        if days:
            start_date = pd.to_datetime(end_date) - pd.Timedelta(days)
            data_df = yf.download(self.tickers, start=start_date, end=end_date).stack(future_stack=True)
            data_df.index.names = ['date', 'ticker']
            data_df.columns = data_df.columns.str.lower()
            self.financial_data = data_df
        elif self.financial_data:
            start_date = self.financial_data['date'].max() + pd.Timedelta(1)
            data_df = yf.download(self.tickers, start=start_date, end=end_date).stack(future_stack=True)
            data_df.index.names = ['date', 'ticker']
            data_df.columns = data_df.columns.str.lower()
            self.financial_data.loc[len(self.financial_data)] = data_df


        