from typing import Callable
import numpy as np
import pandas as pd
import pandas_ta as ta

class Index():
    def __init__(self, name: str):
        self.name = name
        self.tickers = []
        self.gics: dict
        self.financial_data: pd.DataFrame
        self.stocks = dict

    def send_index_data(self, fin_data: pd.DataFrame, tickers: list) -> dict:
        return {'financial_data': fin_data, 'tickers': tickers}
    
    def scrape_gics(self) -> dict:
        gics_dict = {}

        if self.name == 'sp500':
            sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
            gics = pd.read_html(sp500_url)[0]
            gics['Symbol'] = gics['Symbol'].str.replace('.', '-')
            gics_list = gics.to_dict('records')

            for gics_record in gics_list:
                gics_dict[gics_record['Symbol']] = {
                    'security': gics_record['Security'],
                    'sector': gics_record['GICS Sector'],
                    'sub-industry': gics_record['GICS Sub-Industry'],
                    'date_added': gics_record['Date added'],
                    'cik': gics_record['CIK'],
                    'founded': gics_record['Founded']
                }

        return gics_dict
    
        # this will not work for other indexes than sp500
        # method need to be developed for scraping gics data for different indexes

    def set_tickers_and_gics(self, tickers_in_portfolio: Callable[[], list]) -> None:
        new_gics = self.scrape_gics()
        
        if self.gics:
            active_tickers = tickers_in_portfolio()
            portfolio_gics = {key: self.gics[key] for key in active_tickers if key in self.gics}
            new_gics.update(portfolio_gics)

        self.gics = new_gics
        self.tickers = list(self.gics.keys())

        # write functionality for checking if some deprecated tickers are in fin_data
        # but not in tickers and not in portfolio, then remove data from fin_data for those tickers

    def set_fin_data(self, fin_data: pd.DataFrame) -> None:
        if not fin_data.empty:
            if self.financial_data.empty:
                self.financial_data = fin_data
            else:
                hist_fin_data = self.financial_data
                updated_fin_data = pd.concat([hist_fin_data, fin_data])
                updated_fin_data.sort_index(inplace=True)
                self.financial_data = updated_fin_data

    def initialize_stocks(self) -> None:
        stocks_dict = {}
        
        for ticker in self.tickers:
            stock_gics = self.gics[ticker]
            stock_fin_data = self.financial_data.loc[(slice(None), ticker), :]
            stocks_dict[ticker] = Stock(ticker, stock_fin_data, stock_gics)
            stocks_dict[ticker].compute_indicators()

        self.stocks = stocks_dict

    def generate_stock(self, ticker: str):
        pass

    def update_stock_fin_data(self, ticker: str) -> None:

        ################################################################
        # method for updating financial data in stock objects
        # and computing indicators after update
        ################################################################

        stock_fin_data = self.financial_data.loc[(slice(None), ticker), :]
        pass

    def update_stocks(self) -> None:

        ################################################################
        # method for updating stock objects dictionary
        # and computing indicators after update
        ################################################################

        pass
        
    
class Stock:
    def __init__(self, ticker: str, fin_data: pd.DataFrame, gics: pd.DataFrame):
        self.ticker = ticker
        self.financial_data = fin_data
        self.gics = gics

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