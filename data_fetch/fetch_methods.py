import pandas as pd

def sp500():
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    
    sp500.to_csv('../data/sp500.csv', index=False)

    sp500['Symbol'] = sp500['Symbol'].str.replace('.', '-')

    symbols_list = sp500['Symbol'].unique().tolist()
    return symbols_list