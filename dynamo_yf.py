import boto3 as bt
import datetime as dt
import pandas as pd
import yfinance as yf

def initialize_resource():
    dynamodb = bt.resource('dynamodb',
                        aws_access_key_id='dummy',
                        aws_secret_access_key='dummy',
                        region_name='local',
                        endpoint_url='http://localhost:8000')
    
    return dynamodb

def create_financial_data_table() -> None:
    dynamodb = initialize_resource()

    table_creation_response = dynamodb.create_table(
        TableName='financial_data',
        KeySchema=[
            {
                'AttributeName': 'ticker',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'date',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'ticker',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'date',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    print(table_creation_response)

def last_date_adapter(hist_fin_data: pd.DataFrame):
    last_date = pd.to_datetime(hist_fin_data.index.levels[0][-1]) + pd.Timedelta(days=1)
    print('type of adapter return: ', type(last_date))
    return last_date

def download_fin_data(hist_fin_data: pd.DataFrame, tickers: list) -> None:
    if not hist_fin_data.empty:
        start_date = last_date_adapter(hist_fin_data)
    else:
        start_date = dt.date(2016, 1, 1)

    end_date = dt.date.today()
    fin_data = yf.download(tickers, start=start_date, end=end_date, rounding=True).stack(future_stack=True)
    fin_data.reset_index(inplace=True)
    fin_data.columns = fin_data.columns.str.lower()

    return fin_data

def write_fin_data(fin_data: pd.DataFrame) -> None:
    if not fin_data.empty:
        fin_data_records = fin_data.to_dict(orient='records')

        dynamodb = initialize_resource()
        fin_data_table = dynamodb.Table('financial_data')

        with fin_data_table.batch_writer() as batch:
            for record in fin_data_records:
                item = {
                    'ticker': record['ticker'],
                    'date': record['date'].strftime('%Y-%m-%d'),
                    'open': float(record['open']),
                    'high': float(record['high']),
                    'low': float(record['low']),
                    'close': float(record['close']),
                    'adj_close': float(record['adj close']),
                    'volume': int(record['volume']),
                }
                batch.put_item(Item=item)

def send_fin_data(fin_data: pd.DataFrame) -> pd.DataFrame:
    fin_data.set_index(['date', 'ticker'], inplace=True)
    fin_data.sort_index(inplace=True)
    return fin_data
