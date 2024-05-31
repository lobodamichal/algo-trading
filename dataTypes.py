from abc import ABC, abstractmethod
from typing import Callable
import datetime as dt
import numpy as np
import pandas as pd
import pandas_ta as ta

class Subject(ABC):
    def __init__(self):
        self.observers = []

    @abstractmethod
    def register_observer(self, observer):
        pass

    @abstractmethod
    def unregister_observer(self, observer):
        pass

    @abstractmethod
    def notify_observer(self):
        pass

class Observer(ABC):
    @abstractmethod
    def update(self, update_date):
        pass

class Index(Subject):
    def __init__(self, name: str):
        # \? \? \? \? why is this super here \? \? \? \?
        super().__init__()
        self.name = name
        self.tickers = []
        self.gics = {}
        self.stocks = {}
        self.initial_date = dt.date(2024, 5, 27)
        self.last_update = None

    def register_observer(self, observer):
        self.observers.append(observer)

    def unregister_observer(self, observer):
        self.observers.remove(observer)

    def notify_observer(self):
        for observer in self.observers:
            observer.update(self.last_update)

    def set_update_date(self, last_update_date):
        self.last_update = last_update_date
        self.notify_observer()
    
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
            bought_tickers = tickers_in_portfolio()
            portfolio_gics = {key: self.gics[key] for key in bought_tickers if key in self.gics}
            new_gics.update(portfolio_gics)

        self.gics = new_gics
        self.tickers = list(self.gics.keys())
    
    def initialize_stock_objects(self) -> None:
        stocks_dict = {}
        
        for ticker in self.tickers:
            stock_gics = self.gics[ticker]
            #stock_fin_data = self.financial_data.loc[(slice(None), ticker), :]
            stock = Stock(ticker, stock_gics, self.name, self.last_update)
            self.register_observer(stock)
            stocks_dict[ticker] = stock
            #stocks_dict[ticker].compute_indicators()

        self.stocks = stocks_dict

    ################################################################
    # write method for checking if any new stock objects need to be created
    # in case a new ticker is available in index
    ################################################################
    
class Stock(Index, Observer):
    # \? \? \? \? why I need to pass inherited prop in __init__ \? \? \? \?
    # \? \? \? \? can I do it differently                       \? \? \? \?
    # \? \? \? \? how to inherit prop last_update and name      \? \? \? \?

    def __init__(self, ticker: str, gics: dict, index_name: str, last_update):
        self.index_name = index_name
        self.last_update = last_update
        self.ticker = ticker
        self.financial_data = pd.DataFrame()
        self.gics = gics

    def update(self, update_date):
        self.last_update = update_date

    #def set_financial_data(self) 

    ################################################################
    # write functionality for checking if some deprecated tickers are in dynamo_db
    # but not in tickers and not in portfolio, then remove data from dynamo_db for those tickers
    ################################################################
    
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