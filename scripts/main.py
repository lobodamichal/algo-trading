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

sp500_historic_df = tech_indicators.GK_vol(sp500_historic_df)
sp500_historic_df = tech_indicators.RSI(sp500_historic_df)
sp500_historic_df = tech_indicators.B_bands(sp500_historic_df, normalized=False)

msft_data = sp500_historic_df.loc[pd.IndexSlice[:, 'MSFT'], :]
msft_data.reset_index(inplace=True)

print(msft_data)

plot.plot(msft_data)