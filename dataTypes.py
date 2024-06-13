import datetime as dt
from abc import ABC, abstractmethod
from typing import Callable

import numpy as np
import pandas as pd
import pandas_ta as ta

class Subject(ABC):
    """
    Abstract base class to represent the subject in the observer pattern.
    
    Attributes
    ----------
    observers : list
        A list to store observers.
    """
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
    """
    Abstract base class to represent the observer in the observer pattern.
    """
    @abstractmethod
    def update(self, value):
        pass

class Index(Subject):
    """
    A class to represent a stock market index and manage its stocks.

    Attributes
    ----------
    name : str
        The name of the index.
    tickers : list
        List of tickers in the index.
    gics : dict
        Dictionary storing GICS information for each ticker.
    stocks : dict
        Dictionary storing Stock objects for each ticker.
    initial_date : datetime.date
        The initial date for the index. Starting date of financial data download.
    last_update : datetime.date
        The last update date for the index. Ending date of financial data download.
    """
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.tickers = []
        self.gics = {}
        self.stocks = {}
        self.initial_date = dt.date(2024, 5, 27)
        self.last_update = None

    def register_observer(self, observer):
        """
        Register an observer to the index.

        Parameters
        ----------
        observer : Observer
            The observer to register.
        """
        self.observers.append(observer)

    def unregister_observer(self, observer):
        """
        Unregister an observer from the index.

        Parameters
        ----------
        observer : Observer
            The observer to unregister.
        """
        self.observers.remove(observer)

    def notify_observer(self):
        """
        Notify all registered observers with the last update date.
        """
        for observer in self.observers:
            observer.update(self.last_update)

    def set_update_date(self, last_update_date: dt.date):
        """
        Set the last update date and notify observers.

        Parameters
        ----------
        last_update_date : datetime.date
            The last update date to set.
        """
        self.last_update = last_update_date
        self.notify_observer()
    
    def scrape_gics(self) -> dict:
        """
        Scrape tickers and their GICS data for the index from the internet.

        Returns
        -------
        dict
            A dictionary containing GICS information for each ticker.
        """
        # this will not work for other indexes than sp500
        # method need to be developed for scraping gics data for different indexes

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

    def set_tickers_and_gics(self, tickers_in_portfolio: Callable[[], list]) -> None:
        """
        Set the tickers and GICS information for the index.

        Parameters
        ----------
        tickers_in_portfolio : Callable[[], list]
            A function that returns a list of tickers currently in the portfolio.
        """
        new_gics = self.scrape_gics()
        
        if self.gics:
            bought_tickers = tickers_in_portfolio()
            portfolio_gics = {key: self.gics[key] for key in bought_tickers if key in self.gics}
            new_gics.update(portfolio_gics)

        self.gics = new_gics
        self.tickers = list(self.gics.keys())

    def create_stock_objects(self):
        """
        Create Stock objects for each ticker in the index and register them as observers.
        """
        new_tickers = [ticker for ticker in self.tickers if ticker not in self.stocks]
        
        for ticker in new_tickers:
            stock_gics = self.gics[ticker]
            stock = Stock(ticker, stock_gics, self.name, self.last_update)
            self.register_observer(stock)
            self.stocks[ticker] = stock
    
class Stock(Observer):
    """
    A class to represent a stock.

    Attributes
    ----------
    ticker : str
        The ticker symbol of the stock.
    gics : dict
        GICS information for the stock.
    index_name : str
        The name of the index the stock belongs to.
    last_update : datetime.date
        The last update date for the stock.
    financial_data : pandas.DataFrame
        DataFrame to store the financial data of the stock.
    """
    def __init__(self, ticker: str, gics: dict, index_name: str, last_update):
        self.ticker = ticker
        self.gics = gics
        self.index_name = index_name
        self.last_update = last_update
        self.financial_data = pd.DataFrame()

    def update(self, value):
        """
        Update the last update date of the stock.

        Parameters
        ----------
        value : datetime.date
            The new last update date.
        """
        self.last_update = value

    def set_financial_data(self, query_fin_data: Callable[[str, dt.date, dt.date | None], pd.DataFrame]):
        """
        Set the financial data for the stock.

        Parameters
        ----------
        query_fin_data : Callable[[str, datetime.date, datetime.date | None], pandas.DataFrame]
            A function to query financial data for the stock.
        """
        fin_data = query_fin_data(self.ticker, self.last_update, None)
        self.financial_data = pd.concat([self.financial_data, fin_data], axis=0)
        self.financial_data.sort_index(inplace=True)

    # TODO:
    # write functionality for checking if some deprecated tickers are in dynamo_db
    # but not in tickers and not in portfolio, then remove data from dynamo_db for those tickers
    # and remove Stock objects from Index

    def calc_gk_vol(self) -> None:
        """
        Calculate Garman-Klass volatility for the stock.
        """
        self.financial_data = self.financial_data.copy()
        self.financial_data['GK_vol'] = 100 * ((np.log(self.financial_data['high']) - np.log(self.financial_data['low'])) **2) / 2 - (2 * np.log(2) - 1) * ((np.log(self.financial_data['adj close']) - np.log(self.financial_data['open']))**2)

    def calc_rsi(self, length:int=20 ) -> None:
        """
        Calculate Relative Strength Index (RSI) for the stock.

        Parameters
        ----------
        length : int, optional
            The period size for the RSI calculation (default is 20).
        """
        self.financial_data = self.financial_data.copy()
        self.financial_data['RSI'] = ta.rsi(close=self.financial_data['adj close'], length=length)

    def calc_bbands(self, length:int=20) -> None:
        """
        Calculate Bollinger Bands for the stock.

        Parameters
        ----------
        length : int, optional
            The period size for the Bollinger Bands calculation (default is 20).
        """
        self.financial_data = self.financial_data.copy()
        bbands_df = ta.bbands(close=self.financial_data['adj close'], length=length)

        self.financial_data['BB_lower'] = bbands_df.iloc[:,0]
        self.financial_data['BB_middle'] = bbands_df.iloc[:,1]
        self.financial_data['BB_upper'] = bbands_df.iloc[:,2]
        self.financial_data['BB_width'] = bbands_df.iloc[:,3]

    def calc_atr(self, length:int=14) -> None:
        """
        Calculate Average True Range (ATR) for the stock.

        Parameters
        ----------
        length : int, optional
            The period size for the ATR calculation (default is 14).
        """
        self.financial_data = self.financial_data.copy()
        self.financial_data['ATR'] = ta.atr(high=self.financial_data['high'], low=self.financial_data['low'], close=self.financial_data['adj close'], length=length)

    def calc_macd(self, length_fast:int=12, length_slow:int=26, length_signal:int=9) -> None:
        """
        Calculate Moving Average Convergence Divergence (MACD) for the stock.

        Parameters
        ----------
        length_fast : int, optional
            The period size for the fast EMA (default is 12).
        length_slow : int, optional
            The period size for the slow EMA (default is 26).
        length_signal : int, optional
            The period size for the signal line (default is 9).
        """
        self.financial_data = self.financial_data.copy()
        self.financial_data['EMA_fast'] = ta.ema(self.financial_data['adj close'], length=length_fast)
        self.financial_data['EMA_slow'] = ta.ema(self.financial_data['adj close'], length=length_slow)
        self.financial_data['MACD'] = self.financial_data['EMA_fast'] - self.financial_data['EMA_slow']
        self.financial_data['MACD_signal'] = ta.ema(self.financial_data['MACD'], length=length_signal)

    def compute_indicators(self) -> None:
        """
        Compute all technical indicators for the stock.
        """
        self.calc_gk_vol()
        self.calc_rsi()
        self.calc_bbands()
        self.calc_atr()
        self.calc_macd()