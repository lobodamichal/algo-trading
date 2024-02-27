import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_fetch import fetch_methods, fetch_finan_data

sp500_symbols = fetch_methods.sp500()
sp500_historic_df = fetch_finan_data.historic_data(sp500_symbols, 10)