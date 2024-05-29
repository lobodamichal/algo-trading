import datetime as dt
import numpy as np
import pandas as pd
import pandas_ta as ta

class Index():
    def __init__(self, name: str):
        self.name = name
        self.tickers = []
        self.gics: pd.DataFrame
        self.financial_data: pd.DataFrame
        self.stocks = dict

    def fetch_gics(self) -> pd.DataFrame:
        if self.name == 'sp500':
            sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
            gics = pd.read_html(sp500_url)[0]
            gics['Symbol'] = gics['Symbol'].str.replace('.', '-')
        return gics

    def put_tickers(self, gics: pd.DataFrame) -> None:
        self.gics = gics
        self.tickers = gics['Symbol'].unique().tolist()

    def look_for_new_tickers(self, tickers_in_portfolio: list) -> None:
        ################################################################
        # method that checks if a new ticker is available
        # then updates tickers and financial data accordingly
        # keeping deprecated tickers in financial data if they are available in portfolio
        # till it's stock in portfolio will be sold
        ################################################################
        pass

    def update_financial_data(self, fin_data: pd.DataFrame) -> None:
        #start_date = pd.to_datetime(self.financial_data.index.levels[0][-1]) + pd.Timedelta(days=1)
        #end_date = dt.date.today()

        #data_df = yf.download(self.tickers, start=start_date, end=end_date, rounding=True).stack(future_stack=True)
        #fin_data.reset_index(inplace=True)
        #fin_data.columns = fin_data.columns.str.lower()

        if not fin_data.empty:
            hist_fin_data = self.financial_data
            updated_fin_data = pd.concat([hist_fin_data, fin_data])
            updated_fin_data.sort_index(inplace=True)
            self.financial_data = updated_fin_data

    def send_data(self) -> dict:
        return {'financial_data': self.financial_data, 'tickers': self.tickers}
    
    def receive_fin_data(self, fin_data: pd.DataFrame) -> None:
        self.update_financial_data(fin_data)

    def receive_tickers_data(self, tickers: list) -> None:
        ################################################################
        # port method for receiving tickers available in portfolio      
        ################################################################
        pass 

    def generate_stocks(self) -> None:
        stocks_dict = {}
        
        for ticker in self.tickers:
            stock_gics_df = self.gics[self.gics['Symbol'] == ticker]
            stock_gics_dict = stock_gics_df[['Security', 'GICS Sector', 'GICS Sub-Industry',
                'Date added', 'CIK', 'Founded']].to_dict('records')
            
            stock_financial_data_df = self.financial_data.loc[(slice(None), ticker), :]
            stocks_dict[ticker] = Stock(ticker, stock_financial_data_df, stock_gics_dict[0])
            stocks_dict[ticker].compute_indicators()

        self.stocks = stocks_dict

    def update_stocks_fin_data(self) -> None:
        ################################################################
        # method for updating financial data in stock objects
        # and computing indicators after update
        ################################################################
        pass

    '''
    def fetch_hist_financial_data(self, days: int, path: str) -> None:
        #end_date = dt.date.today()
        end_date = dt.date(2024, 5, 5)
        start_date = end_date - pd.Timedelta(days=days)
        
        data_df = yf.download(self.tickers, start=start_date, end=end_date, rounding=True).stack(future_stack=True)
        
        data_df.reset_index(inplace=True)
        data_df.columns = data_df.columns.str.lower()
        data_df.to_csv(path, index=False)
    '''
    '''
    def read_hist_financial_data(self, path: str):
        data_df = pd.read_csv(path)
        data_df.set_index(['date', 'ticker'], inplace=True)
        data_df.sort_index(inplace=True)

        self.financial_data = data_df
    '''
    
class Stock:
    def __init__(self, ticker, history_df, gics_df):
        self.ticker: str = ticker
        self.financial_data: pd.DataFrame = history_df
        self.gics: pd.DataFrame = gics_df

    def GK_vol(self) -> None:
        self.financial_data = self.financial_data.copy()
        self.financial_data['GK_vol'] = 100 * ((np.log(self.financial_data['high']) - np.log(self.financial_data['low'])) **2) / 2 - (2 * np.log(2) - 1) * ((np.log(self.financial_data['adj close']) - np.log(self.financial_data['open']))**2)

    def RSI(self, length:int=20 ) -> None:
        self.financial_data = self.financial_data.copy()
        self.financial_data['RSI'] = ta.rsi(close=self.financial_data['adj close'], length=length)

    def B_bands(self, length:int=20) -> None:
        self.financial_data = self.financial_data.copy()
        bbands_df = ta.bbands(close=self.financial_data['adj close'], length=length)

        self.financial_data['BB_lower'] = bbands_df.iloc[:,0]
        self.financial_data['BB_middle'] = bbands_df.iloc[:,1]
        self.financial_data['BB_upper'] = bbands_df.iloc[:,2]
        self.financial_data['BB_width'] = bbands_df.iloc[:,3]

    def ATR(self, length:int=14) -> None:
        self.financial_data = self.financial_data.copy()
        self.financial_data['ATR'] = ta.atr(high=self.financial_data['high'], low=self.financial_data['low'], close=self.financial_data['adj close'], length=length)

    def MACD(self, length_fast:int=12, length_slow:int=26, length_signal:int=9) -> None:
        self.financial_data = self.financial_data.copy()
        self.financial_data['EMA_fast'] = ta.ema(self.financial_data['adj close'], length=length_fast)
        self.financial_data['EMA_slow'] = ta.ema(self.financial_data['adj close'], length=length_slow)
        self.financial_data['MACD'] = self.financial_data['EMA_fast'] - self.financial_data['EMA_slow']
        self.financial_data['MACD_signal'] = ta.ema(self.financial_data['MACD'], length=length_signal)

    def compute_indicators(self) -> None:
        self.GK_vol()
        self.RSI()
        self.B_bands()
        self.ATR()
        self.MACD()