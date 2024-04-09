import numpy as np
import pandas as pd
import pandas_ta as ta

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

    def update_financial_data(self, financial_data) -> None:
        self.financial_data = financial_data