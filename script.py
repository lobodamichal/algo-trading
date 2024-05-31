from dataTypes import Index
from portfolio import Portfolio
import datetime as dt
import pandas as pd
from dynamo_yf import download_fin_data, query_fin_data_table

################################################################
# new script needed
################################################################

def testIndex():
    sp500 = Index('sp500')
    sp500.scrape_gics()
    print(sp500.gics)

def testWrite():
    sp500 = Index('sp500')
    hist_fin_data = pd.DataFrame()
    tickers = ['AAPL', 'AMZN']

    #create_financial_data_table()
    download_fin_data(tickers, sp500.initial_date, sp500.last_update)

def testStocks():
    sp500 = Index('sp500')
    portfolio = Portfolio(account=10000)
    sp500.set_tickers_and_gics(portfolio.tickers_in_portfolio)
    sp500.tickers = ['AAPL', 'AMZN']

    sp500.create_stock_objects()
    sp500.set_update_date(dt.date(2024, 5, 30))

    #### execute this once a day
    #update_date = download_fin_data(sp500.tickers, sp500.initial_date, sp500.last_update)

    sp500.stocks['AAPL'].set_financial_data(query_fin_data_table)
    print(sp500.stocks['AAPL'].financial_data)
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
testStocks()

