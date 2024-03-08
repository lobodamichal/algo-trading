import numpy as np
import pandas_ta as ta

def normalize(value, normalized):
    if normalized:
        return np.log1p(value)
    else:
        return value

def GK_vol(df):
    df['GK_vol'] = 100 * ((np.log(df['high']) - np.log(df['low'])) **2) / 2 - (2 * np.log(2) - 1) * ((np.log(df['adj close']) - np.log(df['open']))**2)
    return df

def RSI(df):
    df['RSI'] = df.groupby(level=1)['adj close'].transform(lambda x: ta.rsi(close=x, length=20))
    return df

def B_bands(df, lenght=20, normalized=True):
    df['BB_upper'] = df.groupby(level=1)['adj close'].transform(lambda x: ta.bbands(close=normalize(x, normalized), length=lenght).iloc[:,0])
    df['BB_middle'] = df.groupby(level=1)['adj close'].transform(lambda x: ta.bbands(close=normalize(x, normalized), length=lenght).iloc[:,1])
    df['BB_lower'] = df.groupby(level=1)['adj close'].transform(lambda x: ta.bbands(close=normalize(x, normalized), length=lenght).iloc[:,2])
    df['BB_width'] = df.groupby(level=1)['adj close'].transform(lambda x: ta.bbands(close=normalize(x, normalized), length=lenght).iloc[:,3])
    return df