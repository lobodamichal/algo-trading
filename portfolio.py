import pandas as pd

class Portfolio():
    def __init__(self, account: float):
        self.account = account
        self.portfolio = pd.DataFrame(columns=[
                'ticker', 
                'buy_price',
                'buy_date',  
                'quantity', 
                'sell_price', 
                'sell_date'
            ])
        
        self.history = pd.DataFrame(columns=[
                'ticker', 
                'buy_price',
                'buy_date',  
                'quantity', 
                'sell_price', 
                'sell_date'
            ])

    def buy_stock(self, ticker:str, buy_price:float, buy_date:str, quantity:int):
        if not self.portfolio['ticker'].isin([ticker]).any():
            new_record = {
                    'ticker': ticker, 
                    'buy_price': buy_price, 
                    'buy_date': buy_date,
                    'quantity': quantity 
                }
            
            self.account -= buy_price * quantity
            self.portfolio = self.portfolio.append(new_record, ignore_index=True)

    def sell_stock(self, ticker:str, sell_price:float, sell_date:str):
        if self.portfolio['ticker'].isin([ticker]).any():
            index = self.portfolio[self.portfolio['ticker'] == ticker].index[0]
            self.portfolio.at[index, 'sell_price'] = sell_price
            self.portfolio.at[index,'sell_date'] = sell_date
            quantity = self.portfolio.at[index,'quantity']

            self.account += sell_price * quantity

            row = self.portfolio.loc[index]
            self.portfolio.drop(index, inplace=True)
            self.history = self.history.append(row, ignore_index=True)