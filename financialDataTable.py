import datetime as dt
from decimal import Decimal
from typing import Tuple

import boto3 as bt
from boto3.dynamodb.conditions import Key
import pandas as pd
import yfinance as yf

def initialize_resource():
    """
    Initialize the DynamoDB resource.

    Returns
    -------
    dynamodb : boto3.resource
        The DynamoDB resource object.
    """
    dynamodb = bt.resource('dynamodb',
                        aws_access_key_id='dummy',
                        aws_secret_access_key='dummy',
                        region_name='local',
                        endpoint_url='http://localhost:8000')
    return dynamodb

def create_fin_data_table(dynamodb) -> None:
    """
    Create the financial data table in DynamoDB.
    
    This function creates a DynamoDB table with the specified key schema,
    attribute definitions, and provisioned throughput.

    Parameters
    ----------
    dynamodb : boto3.resource
        The DynamoDB resource object.
    """

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

#investigate
def decimal_adapter(value):
    """
    Convert a float to a Decimal for DynamoDB compatibility.

    Parameters
    ----------
    value : float or any
        The value to be converted.

    Returns
    -------
    Decimal or value
        The Decimal value if the input was a float, otherwise the original value.
    """
    if isinstance(value, float):
        return Decimal(str(value))
    return value

def fin_data_df_adapter(table: dict) -> pd.DataFrame:
    """
    Convert a DynamoDB query result to a pandas DataFrame.

    Parameters
    ----------
    table : dict
        The DynamoDB query result.

    Returns
    -------
    pd.DataFrame
        The resulting sorted DataFrame with a multi-index of date and ticker.
    """
    df = pd.DataFrame(table)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index(['date', 'ticker'], inplace=True)
    df.sort_index(inplace=True)
    return df

def download_fin_data(tickers: list, initial_date: dt.date, last_update: dt.date | None) -> Tuple[dt.date, pd.DataFrame]:
    """
    Download financial data from Yahoo Finance and write it to DynamoDB.

    Parameters
    ----------
    tickers : list of strings
        List of stock tickers to download data for.
    initial_date : dt.date
        The initial date to start downloading data from.
    last_update : dt.date or None
        The last update date; if None, the initial date is used.

    Returns
    -------
    Tuple of dt.date and pd.DataFrame
        The current date as the last update date and downloaded financial data from Yahoo Finance.
    """
    
    if last_update:
        start_date = last_update + dt.timedelta(days=1)
    else:
        start_date = initial_date

    today_date = dt.date.today()
    fin_data = yf.download(tickers, start=start_date, end=today_date, rounding=True).stack(future_stack=True)
    fin_data.reset_index(inplace=True)
    fin_data.columns = fin_data.columns.str.lower()

    return today_date, fin_data

def write_to_fin_data_table(fin_data: pd.DataFrame, dynamodb) -> None:
    """
    Write financial data to the DynamoDB table.

    Parameters
    ----------
    fin_data : pd.DataFrame
        The financial data to write.
    dynamodb : boto3.resource
        The DynamoDB resource object.
    """
    if not fin_data.empty:
        fin_data_records = fin_data.to_dict(orient='records')

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

def query_fin_data_table(ticker: str, start_date: dt.date, end_date: dt.date | None , dynamodb) -> pd.DataFrame:
    """
    Query financial data from the DynamoDB table.

    Parameters
    ----------
    ticker : str
        The stock ticker to query data for.
    start_date : dt.date
        The start date for the query.
    end_date : dt.date or None
        The end date for the query; if None, today's date is used.
    dynamodb : boto3.resource
        The DynamoDB resource object.

    Returns
    -------
    pd.DataFrame
        The queried financial data as a DataFrame.
    """
    if not end_date:
        end_date = dt.date.today()

    financial_data_table = dynamodb.Table('financial_data')

    str_start_date = start_date.strftime('%Y-%m-%d')
    str_end_date = end_date.strftime('%Y-%m-%d')

    response = financial_data_table.query(
        KeyConditionExpression=Key('ticker').eq(ticker) & Key('date').between(str_start_date, str_end_date)
    )
    
    return fin_data_df_adapter(response['Items'])
    