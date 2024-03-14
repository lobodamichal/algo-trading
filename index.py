import datetime as dt
import pandas as pd
from stock import Stock
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

    def fetch_financial_data(self, days: int) -> None:
        end_date = dt.date.today()
        start_date = pd.to_datetime(end_date) - pd.Timedelta(days=days)
        data_df = yf.download(self.tickers, start=start_date, end=end_date).stack(future_stack=True)
        data_df.index.names = ['date', 'ticker']
        data_df.columns = data_df.columns.str.lower()

        self.financial_data = data_df

    def update_financial_data(self) -> None:
        end_date = dt.date.today()
        start_date = self.financial_data['date'].max() + pd.Timedelta(1)
        data_df = yf.download(self.tickers, start=start_date, end=end_date).stack(future_stack=True)
        data_df.index.names = ['date', 'ticker']
        data_df.columns = data_df.columns.str.lower()

        self.financial_data.loc[len(self.financial_data)] = data_df

    def generate_stocks(self) -> dict:
        stocks_dict = {}
        for ticker in self.tickers:
            stock_gics_df = self.gics[self.gics['Symbol'] == ticker]
            stock_gics_dict = stock_gics_df[['Security', 'GICS Sector', 'GICS Sub-Industry',
                'Date added', 'CIK', 'Founded']].to_dict('records')
            
            stock_financial_data_df = self.financial_data.loc[(slice(None), ticker), :]
            stocks_dict[ticker] = Stock(ticker, stock_financial_data_df, stock_gics_dict[0])
            stocks_dict[ticker].compute_indicators()

        return stocks_dict
    
