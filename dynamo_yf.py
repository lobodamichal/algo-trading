import boto3 as bt
import datetime as dt
from decimal import Decimal
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

def download_fin_data(tickers: list, initial_date: dt.date, last_update) -> dict:

    if last_update:
        start_date = last_update + dt.timedelta(days=1)
    else:
        start_date = initial_date

    today_date = dt.date.today()
    fin_data = yf.download(tickers, start=start_date, end=today_date, rounding=True).stack(future_stack=True)
    fin_data.reset_index(inplace=True)
    fin_data.columns = fin_data.columns.str.lower()

    write_fin_data(fin_data)

    return {
        'last_update': today_date
    }

def decimal_adapter(x):
    if isinstance(x, float):
        return Decimal(str(x))
    return x

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
                    'open': decimal_adapter(record['open']),
                    'high': decimal_adapter(record['high']),
                    'low': decimal_adapter(record['low']),
                    'close': decimal_adapter(record['close']),
                    'adj_close': decimal_adapter(record['adj close']),
                    'volume': int(record['volume']),
                }
                batch.put_item(Item=item)
