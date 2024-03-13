from index import Index
from plot import Plot
from stock import Stock

sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies' 

sp500 = Index('sp500')
sp500.fetch_tickers(sp500_url)
sp500.fetch_financial_data(days=365)

stocks_dict = sp500.generate_stocks()

stocks_dict['AAPL'].compute_indicators()

plot = Plot()
plot.plot(stocks_dict['AAPL'], days=150)