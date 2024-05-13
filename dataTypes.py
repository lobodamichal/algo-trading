import datetime as dt
import numpy as np
import pandas as pd
import pandas_ta as ta
import yfinance as yf

class Index():
    def __init__(self, name: str):
        self.name = name
        self.tickers = []
        self.gics: pd.DataFrame
        self.financial_data: pd.DataFrame
        self.stocks = dict

        self.sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies' 

    def fetch_tickers(self, url: str) -> None:
        tickers_df = pd.read_html(url)[0]
        tickers_df['Symbol'] = tickers_df['Symbol'].str.replace('.', '-')

        self.gics = tickers_df
        self.tickers = tickers_df['Symbol'].unique().tolist()

    def fetch_hist_financial_data(self, days: int, path: str) -> None:
        #end_date = dt.date.today()
        end_date = dt.date(2024, 5, 5)
        start_date = end_date - pd.Timedelta(days=days)
        
        data_df = yf.download(self.tickers, start=start_date, end=end_date, rounding=True).stack(future_stack=True)
        
        data_df.reset_index(inplace=True)
        data_df.columns = data_df.columns.str.lower()
        data_df.to_csv(path, index=False)

    def update_financial_data(self, path: str) -> None:
        start_date = pd.to_datetime(self.financial_data.index.levels[0][-1]) + pd.Timedelta(days=1)
        end_date = dt.date.today()

        data_df = yf.download(self.tickers, start=start_date, end=end_date, rounding=True).stack(future_stack=True)
        data_df.reset_index(inplace=True)
        data_df.columns = data_df.columns.str.lower()

        if not data_df.empty:
            data_df.set_index(['date', 'ticker'], inplace=True)
            data_df.sort_index(inplace=True)
            self.financial_data = pd.concat([self.financial_data, data_df])
            self.financial_data.to_csv(path)

    def read_hist_financial_data(self, path: str):
        data_df = pd.read_csv(path)
        data_df.set_index(['date', 'ticker'], inplace=True)
        data_df.sort_index(inplace=True)

        self.financial_data = data_df

    def generate_stocks(self):
        stocks_dict = {}
        
        for ticker in self.tickers:
            stock_gics_df = self.gics[self.gics['Symbol'] == ticker]
            stock_gics_dict = stock_gics_df[['Security', 'GICS Sector', 'GICS Sub-Industry',
                'Date added', 'CIK', 'Founded']].to_dict('records')
            
            stock_financial_data_df = self.financial_data.loc[(slice(None), ticker), :]
            stocks_dict[ticker] = Stock(ticker, stock_financial_data_df, stock_gics_dict[0])
            stocks_dict[ticker].compute_indicators()

        self.stocks = stocks_dict

    def update_stocks(self):
        ################################################################
        pass
    
class Stock:
    def __init__(self, ticker, history_df, gics_df):
        self.ticker: str = ticker
        self.financial_data: pd.DataFrame = history_df
        self.gics: pd.DataFrame = gics_df

    def GK_vol(self) -> None:
        self.financial_data = self.financial_data.copy()
        self.financial_data['GK_vol'] = 100 * ((np.log(self.financial_data['high']) - np.log(self.financial_data['low'])) **2) / 2 - (2 * np.log(2) - 1) * ((np.log(self.financial_data['adj close']) - np.log(self.financial_data['open']))**2)

    def RSI(self, length=20) -> None:
        self.financial_data = self.financial_data.copy()
        self.financial_data['RSI'] = ta.rsi(close=self.financial_data['adj close'], length=length)

    def B_bands(self, lenght=20) -> None:
        self.financial_data = self.financial_data.copy()
        bbands_df = ta.bbands(close=self.financial_data['adj close'], length=lenght)

        self.financial_data['BB_lower'] = bbands_df.iloc[:,0]
        self.financial_data['BB_middle'] = bbands_df.iloc[:,1]
        self.financial_data['BB_upper'] = bbands_df.iloc[:,2]
        self.financial_data['BB_width'] = bbands_df.iloc[:,3]

    def ATR(self, length=14) -> None:
        self.financial_data = self.financial_data.copy()
        self.financial_data['ATR'] = ta.atr(high=self.financial_data['high'], low=self.financial_data['low'], close=self.financial_data['adj close'], length=length)

    def MACD(self) -> None:
        self.financial_data = self.financial_data.copy()
        #had error for signalma == NoneType
        #self.financial_data['MACD'] = ta.macd(self.financial_data['adj close']).iloc[:,0]
        
        self.financial_data['EMA_fast'] = ta.ema(self.financial_data['adj close'], length=12)
        self.financial_data['EMA_slow'] = ta.ema(self.financial_data['adj close'], length=26)
        self.financial_data['MACD'] = self.financial_data['EMA_fast'] - self.financial_data['EMA_slow']
        self.financial_data['MACD_signal'] = ta.ema(self.financial_data['MACD'], length=9)

    def compute_indicators(self) -> None:
        self.GK_vol()
        self.RSI()
        self.B_bands()
        self.ATR()
        self.MACD()