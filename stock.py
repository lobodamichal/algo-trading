import numpy as np
import pandas as pd
import pandas_ta as ta

class Stock:
    def __init__(self, ticker, df):
        self.ticker: str = ticker
        self.history: pd.DataFrame = df

    def GK_vol(self) -> None:
        self.history['GK_vol'] = 100 * ((np.log(self.history['high']) - np.log(self.history['low'])) **2) / 2 - (2 * np.log(2) - 1) * ((np.log(self.history['adj close']) - np.log(self.history['open']))**2)

    def RSI(self, length=20) -> None:
        self.history['RSI'] = ta.rsi(close=self.history['adj close'], length=length)

    def B_bands(self, lenght=20) -> None:
        bbands_df = ta.bbands(close=self.history['adj close'], length=lenght)
        if bbands_df:
            self.history['BB_lower'] = bbands_df.iloc[:,0]
            self.history['BB_middle'] = bbands_df.iloc[:,1]
            self.history['BB_upper'] = bbands_df.iloc[:,2]
            self.history['BB_width'] = bbands_df.iloc[:,3]

    def ATR(self, length=14) -> None:
        self.history['ATR'] = ta.atr(high=self.history['high'], low=self.history['low'], close=self.history['adj close'], length=length)

    def MACD(self, length=14) -> None:
        macd = ta.macd(close=self.history['adj close'],length=length)
        if macd:
            self.history['MACD'] = macd.iloc[:,0]

    def compute_indicators(self) -> None:
        self.GK_vol()
        self.RSI()
        self.B_bands()
        self.ATR()
        self.MACD()