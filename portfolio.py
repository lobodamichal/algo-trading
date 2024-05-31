from matplotlib.style import available
import pandas as pd
class Portfolio():
    def __init__(self, account: float):
        self.account = account
        self.tickers = []

        self.share_to_buy = pd.DataFrame(columns=['ticker', 'price','shares_to_buy'])

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
        
    def set_tickers(self, tickers: list):
        self.tickers = tickers
        
    def tickers_in_portfolio(self) -> list:
        return self.portfolio['ticker'].to_list()
        
    def calculate_shares_to_buy(self, hist_data:pd.DataFrame):
        self.share_to_buy = pd.DataFrame(columns=['ticker', 'price','shares_to_buy'])

        last_date = hist_data.index.levels[0][-1]
        last_date_df = hist_data.loc[(last_date, slice(None)), :]
        #ALTERNATIVE
        #last_date_df = hist_data.xs(last_date)

        tickers_in_portfolio = self.portfolio['ticker'].to_list()
        available_tickers = [ticker for ticker in self.tickers if ticker not in tickers_in_portfolio]

        last_date_df = last_date_df[last_date_df.index.get_level_values('ticker').isin(available_tickers)]
        last_date_df.sort_values(by=['close'], ascending=False, inplace=True)

        

        '''
        for ticker in available_tickers:
            row = pd.DataFrame({'ticker': [ticker], 'price': [price], 'shares_to_buy': [shares_to_buy]})
            self.share_to_buy = pd.concat([self.share_to_buy, row], ignore_index=True)
        '''
    def buy_stock(self, ticker:str, buy_price:float, buy_date:str):
        shares_available = self.share_to_buy[self.share_to_buy['shares_to_buy'] > 0]

        if not self.portfolio['ticker'].isin([ticker]).any() and shares_available['ticker'].isin([ticker]).any():
            quantity = self.share_to_buy.loc[self.share_to_buy['ticker'] == ticker]['shares_to_buy'].iloc[0]
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

            row = self.portfolio.loc[index].to_frame()
            self.history = pd.concat([self.history, row], ignore_index=True)
            self.portfolio.drop(index, inplace=True)