import datetime as dt
from decimal import Decimal

import boto3 as bt
from boto3.dynamodb.conditions import Key
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

def decimal_adapter(value):
    if isinstance(value, float):
        return Decimal(str(value))
    return value

def fin_data_df_adapter(table: dict) -> pd.DataFrame:
    df = pd.DataFrame(table)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index(['date', 'ticker'], inplace=True)
    df.sort_index(inplace=True)
    return df

def download_fin_data(tickers: list, initial_date: dt.date, last_update: dt.date | None) -> dt.date:

    if last_update:
        start_date = last_update + dt.timedelta(days=1)
    else:
        start_date = initial_date

    today_date = dt.date.today()
    fin_data = yf.download(tickers, start=start_date, end=today_date, rounding=True).stack(future_stack=True)
    fin_data.reset_index(inplace=True)
    fin_data.columns = fin_data.columns.str.lower()

    write_fin_data(fin_data)

    return today_date

def write_fin_data(fin_data: pd.DataFrame) -> None:
    if not fin_data.empty:
        fin_data_records = fin_data.to_dict(orient='records')

        # \? \? \? \? should I initialize dynamo resource every time \? \? \? \? 
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

def query_fin_data_table(ticker: str, start_date: dt.date, end_date: dt.date | None ) -> pd.DataFrame:
    if not end_date:
        end_date = dt.date.today()
    
    dynamodb = initialize_resource()
    financial_data_table = dynamodb.Table('financial_data')

    response = financial_data_table.query(
        KeyConditionExpression=Key('ticker').eq(ticker) & Key('date').between(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    )
    
    return fin_data_df_adapter(response['Items'])
    