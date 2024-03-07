import numpy as np

def GK_vol(df):
    df['GK_vol'] = 100 * ((np.log(df['high']) - np.log(df['low'])) **2) / 2 - (2 * np.log(2) - 1) * ((np.log(df['adj close']) - np.log(df['open']))**2)
    return df