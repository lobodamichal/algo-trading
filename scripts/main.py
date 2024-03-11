from locale import normalize
import os
import sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_fetch import fetch_methods, fetch_finan_data
from indicators import tech_indicators
from plots import plot

sp500_symbols = fetch_methods.sp500()
sp500_historic_df = fetch_finan_data.historic_data("sp500", sp500_symbols, 180)

aapl_data = sp500_historic_df.loc[pd.IndexSlice[:, 'AAPL'], :]

aapl_data = tech_indicators.GK_vol(aapl_data)
aapl_data = tech_indicators.RSI(aapl_data)
aapl_data = tech_indicators.B_bands(aapl_data)
aapl_data = tech_indicators.ATR(aapl_data)
aapl_data = tech_indicators.MACD(aapl_data)

aapl_data.reset_index(inplace=True)

print(aapl_data)

plot.plot(aapl_data, label='AAPL')

aapl_data.to_excel('../data/aapl.xlsx')