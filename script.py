from dataTypes import Index
from plot import Plot
from portfolio import Portfolio

def testPlot():
    sp500 = Index('sp500')

    sp500.fetch_tickers(sp500.sp500_url)
    #sp500.fetch_hist_financial_data(days=4*365, path='./data/sp500.xlsx')
    sp500.read_hist_financial_data(path='./data/sp500.xlsx')
    stocks_dict = sp500.generate_stocks()

    plot = Plot()
    plot.plot(stocks_dict['AAPL'], days=90)

def createTable():
    ddb = bt.resource('dynamodb',
                        endpoint_url='http://localhost:8000',
                        region_name='dummy',
                        aws_access_key_id='dummy',
                        aws_secret_access_key='dummy')

    # Create the DynamoDB table.
    ddb.create_table(
            TableName='test',
            AttributeDefinitions=[
                {
                    'AttributeName': 'date',
                    'AttributeType': 'S'
                }
            ],
            KeySchema=[
                {
                    'AttributeName': 'date',
                    'KeyType': 'HASH'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

    table = ddb.Table('test')
    input={'date': '2024-03-12', 'ticker': 'TST', 'close': 1234}
    table.put_item(Item=input)

    scanResponse = table.scan(TableName='test')
    items = scanResponse['Items']
    for item in items:
        print(item)

def testPortfolio():
    sp500 = Index('sp500')

    sp500.fetch_tickers(sp500.sp500_url)
    #sp500.fetch_hist_financial_data(days=4*365, path='./data/sp500.xlsx')
    sp500.read_hist_financial_data(path='./data/sp500.xlsx')
    stocks_dict = sp500.generate_stocks()

    portfolio = Portfolio(account=10000, tickers=list(stocks_dict.keys()))
    portfolio.calculate_shares_to_buy(sp500.financial_data)
    
    
#testPortfolio()
testPlot()