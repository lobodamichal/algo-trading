import numpy as np
import pandas_ta as ta

def GK_vol(df):
    df['GK_vol'] = 100 * ((np.log(df['high']) - np.log(df['low'])) **2) / 2 - (2 * np.log(2) - 1) * ((np.log(df['adj close']) - np.log(df['open']))**2)
    return df

def RSI(df, length=20):
    df['RSI'] = ta.rsi(close=df['adj close'], length=length)
    return df

def B_bands(df, lenght=20):
    bbands_df = ta.bbands(close=df['adj close'], length=lenght)
    df['BB_lower'] = bbands_df.iloc[:,0]
    df['BB_middle'] = bbands_df.iloc[:,1]
    df['BB_upper'] = bbands_df.iloc[:,2]
    df['BB_width'] = bbands_df.iloc[:,3]
    return df

def ATR(df, length=14):
    df['ATR'] = ta.atr(high=df['high'], low=df['low'], close=df['adj close'], length=length)
    return df

def MACD(df, length=14):
    df['MACD'] = ta.macd(close=df['adj close'],length=length).iloc[:,0]
    return df