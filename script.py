from dataTypes import Index
from plot import Plot
from portfolio import Portfolio


################################################################
# new script needed
################################################################

def testIndex():
    sp500 = Index('sp500')
    sp500.scrape_gics()
    print(sp500.gics)

'''
def testPlot():
    sp500 = Index('sp500')

    sp500.fetch_tickers(sp500.sp500_url)
    #sp500.fetch_hist_financial_data(days=4*365, path='./data/sp500.csv')
    sp500.read_hist_financial_data(path='./data/sp500.csv')
    stocks_dict = sp500.generate_stocks()

    plot = Plot()
    plot.plot(stocks_dict['AAPL'], days=48)
    
def testPortfolio():
    sp500 = Index('sp500')

    sp500.fetch_tickers(sp500.sp500_url)
    #sp500.fetch_hist_financial_data(days=4*365, path='./data/sp500.csv')
    sp500.read_hist_financial_data(path='./data/sp500.csv')
    stocks_dict = sp500.generate_stocks()

    portfolio = Portfolio(account=10000, tickers=list(stocks_dict.keys()))
    portfolio.calculate_shares_to_buy(sp500.financial_data)
    
def testUpload():
    sp500 = Index('sp500')

    sp500.fetch_tickers(sp500.sp500_url)
    sp500.fetch_hist_financial_data(days=4*365, path='./data/sp500.csv')
    sp500.read_hist_financial_data(path='./data/sp500.csv')
    sp500.update_financial_data(path='./data/sp500.csv')
    sp500.generate_stocks()


#testPortfolio()
#testPlot()
testUpload()
'''
testIndex()

