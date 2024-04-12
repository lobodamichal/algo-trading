import pandas as pd
import yfinance as yf

class Portfolio():
    def __init__(self, account: float, tickers: list):
        self.account = account
        self.tickers = tickers

        self.equal_weight = pd.DataFrame(columns=['ticker', 'price','shares_to_buy'])

        self.portfolio = pd.DataFrame(columns=[
                'ticker', 
                'buy_price',
                'buy_date',  
                'quantity'
            ])
        
        self.history = pd.DataFrame(columns=[
                'ticker', 
                'buy_price',
                'buy_date',  
                'quantity', 
                'sell_price', 
                'sell_date'
            ])
        
    def calculate_shares_to_buy(self, hist_data:pd.DataFrame):
        self.equal_weight = pd.DataFrame(columns=['ticker', 'price','shares_to_buy'])
        last_date = hist_data.index.levels[0][-1]
        last_date_data = hist_data.xs(last_date)

        for ticker in self.tickers:
            price = last_date_data.loc[ticker, 'close']
            tickers_in_portfolio = self.portfolio['ticker'].to_list()
            tickers_to_buy = [ticker for ticker in self.tickers if ticker not in tickers_in_portfolio]
            shares_to_buy = int(self.account / len(tickers_to_buy) / price)

            row = pd.DataFrame({'ticker': [ticker], 'price': [price], 'shares_to_buy': [shares_to_buy]})
            self.equal_weight = pd.concat([self.equal_weight, row], ignore_index=True)

    def buy_stock(self, ticker:str, buy_price:float, buy_date:str):
        shares_available = self.equal_weight[self.equal_weight['shares_to_buy'] > 0]

        if not self.portfolio['ticker'].isin([ticker]).any() and shares_available['ticker'].isin([ticker]).any():
            quantity = self.equal_weight.loc[self.equal_weight['ticker'] == ticker, 'shares_to_buy']
            self.account -= buy_price * quantity

            row = pd.DataFrame({'ticker': [ticker], 
                                'buy_price': [buy_price], 
                                'buy_date': [buy_date],
                                'quantity': [quantity]
                                })
            self.portfolio = pd.concat([self.portfolio, row], ignore_index=True)

    def sell_stock(self, ticker:str, sell_price:float, sell_date:str):
        if self.portfolio['ticker'].isin([ticker]).any():
            index = self.portfolio[self.portfolio['ticker'] == ticker].index[0]
            self.portfolio.at[index, 'sell_price'] = sell_price
            self.portfolio.at[index, 'sell_date'] = sell_date
            quantity = self.portfolio.at[index, 'quantity']

            self.account += sell_price * quantity

            row = self.portfolio.loc[index].to_frame().T
            self.history = pd.concat([self.history, row], ignore_index=True)
            self.portfolio.drop(index, inplace=True)