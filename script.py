from index import Index
from plot import Plot

sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies' 

sp500 = Index('^GSPC')
sp500.fetch_tickers(sp500_url)
